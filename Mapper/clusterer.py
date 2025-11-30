import numpy as np
from sklearn.cluster import KMeans
import re
import os
import contextlib


# --- [Step 2] 레이어 패턴 클러스터링 및 Candidate 조합들 생성 클래스 ---
class PatternClusterer:
  def __init__(self, layers):
        self.layers = layers
        self.cluster_info = {}

        # [자동 생성] 가능한 모든 유효 Shape을 계산하여 등록
        # 물리적 PE 100% 활용 가능한 Shape + 병렬 처리용 작은 Shape 포함
        self.representative_shapes = self._init_all_possible_shapes()

  def _init_all_possible_shapes(self):
        """
        128x128 (16,384 PEs) 배열에서 가능한 모든 Logical Shape 생성
        """
        shapes = []
        TOTAL_PES = 128 * 128

        # 1. Full Utilization Shapes
        # R을 4부터 증가시키며 찾음
        # 예: 4x4096, 8x2048 ... 128x128 ... 4096x4
        for r in range(4, TOTAL_PES + 1, 4):
            if TOTAL_PES % r == 0:
                c = TOTAL_PES // r
                shapes.append((r, c))

        # 2. High Parallelism Shapes
        # 물리 배열을 2, 4, 8, 16등분 했을 때 나오는 Shape들
        # 예: 16384 / 2 = 8192 PEs, 16384 / 4 = 4096 PEs ...
        divisors = [2, 4, 8, 16]
        for d in divisors:
            sub_pes = TOTAL_PES // d
            for r in range(4, sub_pes + 1, 4):
                if sub_pes % r == 0:
                    c = sub_pes // r
                    # 중복 방지
                    if (r, c) not in shapes:
                        shapes.append((r, c))

        print(f"[System] Shape 초기화 완료: 총 {len(shapes)}개의 논리적 형태 탐색 가능.")

        print("   ㄴ 생성된 Shapes:")
        shapes_str = [str(s) for s in shapes]
        # 한 줄에 10개씩 출력
        for i in range(0, len(shapes_str), 10):
            print(f"      {', '.join(shapes_str[i:i+10])}")

        print(f" ")
        return shapes

  def _match_shapes_by_ratio(self, avg_m, avg_n):
        """ (M, N) 비율에 따라 representative_shapes 정렬 """
        target_ratio = avg_m / avg_n if avg_n > 0 else 1.0
        scored_shapes = []
        for shape in self.representative_shapes:
            r, c = shape
            shape_ratio = r / c
            distance = abs(np.log(target_ratio) - np.log(shape_ratio))
            scored_shapes.append((distance, shape))
        scored_shapes.sort(key=lambda x: x[0])
        return [x[1] for x in scored_shapes]

  def _generate_candidates_for_cluster(self, c_m, c_n, c_k, desc, modality_hints):
        """
        클러스터 특성과 1단계 가이드를 결합하여 Candidate 조합 생성
        """
        candidates = []
        TOTAL_PES = 128 * 128  # 16384

        # 1. 비율 기반 Shape 선정
        matched_shapes = self._match_shapes_by_ratio(c_m, c_n)

        # Modality Hint 적용
        has_text = 'Text' in modality_hints
        has_image = 'Image' in modality_hints

        if has_text and c_n < 128:
             prioritized = [(512, 32), (384, 32)]
             for p in prioritized:
                 if p in matched_shapes:
                     matched_shapes.remove(p)
                     matched_shapes.insert(0, p)
        elif has_image:
             prioritized = [(128, 128), (256, 64)]
             for p in prioritized:
                 if p in matched_shapes:
                     matched_shapes.remove(p)
                     matched_shapes.insert(0, p)

        # Top 3 Shapes 선정
        target_shapes = matched_shapes[:3]

        # Dataflow 결정
        flows = ['WS', 'OS'] if c_k > 1024 else ['OS', 'WS']

        # 2. 병렬 처리 탐색 전략
        # 내림차순 탐색: x4(고효율) -> x2 -> x1
        possible_parallels = [4, 2, 1]

        for shape in target_shapes:
            r, c = shape
            shape_pes = r * c

            # 이 Shape으로 물리적으로 가능한 최대 병렬 개수 계산
            max_physical_par = TOTAL_PES // shape_pes
            if max_physical_par == 0: max_physical_par = 1 # Safety

            for par in possible_parallels:
                # 1) 물리적 한계 체크
                if par > max_physical_par:
                    continue

                # 2) PE 활용률(Utilization) 체크
                # 활용률이 50% 미만인 비효율적 조합은 제외
                # 예: (64, 64) Shape은 PE=4096.
                # x4 -> util=1.0 (통과), x2 -> util=0.5 (통과), x1 -> util=0.25 (제외!)

                utilization = (shape_pes * par) / TOTAL_PES

                # 예외 조건: 해당 Shape이 너무 커서 원래 x1밖에 안 되는 경우(max_physical_par == 1)는 허용
                if utilization < 0.5 and max_physical_par > 1:
                    continue

                # 유효한 조합 추가
                for flow in flows:
                    cand = {'shape': shape, 'parallel': par, 'flow': flow}
                    if cand not in candidates:
                        candidates.append(cand)

        # 3. 후보가 부족할 경우 보정
        # 너무 큰 Shape이라서 x1밖에 안 들어가거나 해서 후보가 적으면, 작은 Shape 강제 추가
        if len(candidates) < 3:
            fallback_shape = (64, 64) # 작아서 병렬화하기 좋은 Shape
            candidates.append({'shape': fallback_shape, 'parallel': 4, 'flow': 'OS'})
            candidates.append({'shape': (128, 64), 'parallel': 2, 'flow': 'WS'})

        return candidates[:6]

  def cluster_layers_and_assign_config(self, n_clusters=4):
        """ [2단계] 클러스터링 수행 """
        print(f"=== [2단계] 레이어 클러스터링 (K={n_clusters}) 및 Candidate 조합 할당 ===")

        # Feature: Log Scale로 변환하여 크기 차이 완화
        features = []
        for layer in self.layers:
            features.append([
                np.log1p(layer['M']), np.log1p(layer['N']), np.log1p(layer['K'])
            ])

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_ids = kmeans.fit_predict(features)
        centroids = kmeans.cluster_centers_

        self.cluster_info = {}

        # 클러스터별 모달리티 분포 파악
        print(f"\n[클러스터 분석 결과]")
        for cid in range(n_clusters):
            indices = [i for i, x in enumerate(cluster_ids) if x == cid]

            # 해당 클러스터에 어떤 모달리티들이 섞여 있는지 파악
            modality_counts = {}
            for i in indices:
                m = self.layers[i]['modality']
                modality_counts[m] = modality_counts.get(m, 0) + 1

            c_m = np.expm1(centroids[cid][0])
            c_n = np.expm1(centroids[cid][1])
            c_k = np.expm1(centroids[cid][2])

            desc = f"Avg(M={int(c_m)}, N={int(c_n)}, K={int(c_k)})"

            # 후보군 생성
            candidates = self._generate_candidates_for_cluster(c_m, c_n, c_k, desc, modality_counts)
            self.cluster_info[cid] = candidates

            print(f"Cluster {cid}: {desc}")
            for i, cand in enumerate(candidates):
                print(f"      [{i+1}] {cand['shape']} x{cand['parallel']} ({cand['flow']})")
            print("-" * 50)

        # 레이어 할당
        for idx, layer in enumerate(self.layers):
            layer['cluster_id'] = cluster_ids[idx]
            layer['assigned_candidates'] = self.cluster_info[cluster_ids[idx]]

        print("\n=== 2단계 완료 ===\n")
        return self.layers

  def export_hcp_table(self):
        print(f"{'LayerID':<8} | {'Modality':<6} | {'M,N,K':<13} | {'Cluster':<6}")
        print("-" * 90)
        for layer in self.layers:
            dims = f"{layer['M']},{layer['N']},{layer['K']}"
            print(f"{layer['id']:<8} | {layer['modality']:<6} | {dims:<15} | {layer['cluster_id']:<7}")

if __name__ == "__main__":

    if 'ModalityStrategist' in globals():
        strategist = ModalityStrategist("output.log")

        with open(os.devnull, 'w') as fnull:
            with contextlib.redirect_stdout(fnull):
              strategist.upload_and_parse_log()
              layers = strategist.aware_modality()

        if layers:
            clusterer = PatternClusterer(layers)
            clusterer.cluster_layers_and_assign_config(n_clusters=4)
            clusterer.export_hcp_table()
        else:
            print("[Error] 로그 파일에서 데이터를 읽지 못했습니다.")
    else:
        print("[Error] ModalityStrategist 클래스를 찾을 수 없습니다.")
