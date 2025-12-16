import numpy as np
import math
import csv

# Colab 환경 여부 확인 및 다운로드 함수 임포트
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# --- [Step 3] 각 클러스터별로 최적의 하드웨어 재구성 조합 결정 후 Hardware Configuration Table 에 저장하는 클래스
class ClusterOptimizer:
    def __init__(self, layers_with_candidates):
        self.layers = layers_with_candidates
        self.hcp_table = {} # Config_ID -> Config Details

    def _estimate_runtime(self, layer, config):
        """
        [비용 함수]: "Compute Bound vs Memory Bound" 중 bottleneck 지점 찾기
        """
        M, N, K = layer['M'], layer['N'], layer['K']

        # Config 파싱
        R_l, C_l = config['shape']
        parallel = config['parallel']
        flow = config['flow']

        # 1. 공간 분할 (Spatial Partitioning) 적용
        # 작업을 병렬 개수만큼 나눔.
        # 올림(ceil) 처리 -> 작업이 균등하게 안 나뉘면 늦게 끝나는 작업이 전체 시간 결정
        M_core = math.ceil(M / parallel)

        # 2. [Compute Cycles] 계산 (이상적인 연산 시간 / 활용률)
        # 총 연산량 (MACs)
        total_ops = M_core * N * K

        # 물리적 PE 활용률 (Utilization) 계산
        # 논리적 Shape 타일에 딱 맞아떨어지지 않는 부분은 낭비됨
        tile_m = math.ceil(M_core / R_l) * R_l
        tile_n = math.ceil(N / C_l) * C_l

        utilization = (M_core * N) / (tile_m * tile_n)

        # 총 물리 PE 수 (서브 어레이 1개 기준)
        phys_pes = R_l * C_l

        # Compute Latency = (연산량 / PE수) / 활용률
        compute_cycles = (total_ops / phys_pes) / utilization

        # 3. [Memory Cycles] 계산 (데이터 이동량 / 대역폭)
        # Dataflow에 따라 DRAM에서 가져와야 할 데이터 양이 다름
        # OS: Input + Weight 로딩, Output은 온칩 누적 (DRAM 쓰기 최소화)
        # WS: Input + Output 이동, Weight는 고정 (DRAM 읽기 최소화)

        # 데이터의 양에 비례
        if flow == 'OS':
            # Output 고정 -> Input(M*K) + Weight(K*N) 이동
            traffic = (M_core * K) + (K * N)
        elif flow == 'WS':
            # Weight 고정 -> Input(M*K) + Output(M*N) 이동
            traffic = (M_core * K) + (M_core * N)
        else: # IS (Input Stationary)
            traffic = (K * N) + (M_core * N)

        # 대역폭 상수 (임의값, 상대 비교용)
        BANDWIDTH_PER_CYCLE = 64 # 사이클당 64개 데이터 전송 가능
        memory_cycles = traffic / BANDWIDTH_PER_CYCLE

        # 4. [Bottleneck Analysis] 더블 버퍼링 효과
        # 이상적인 경우: max(Compute, Memory)가 전체 시간을 결정 (Hiding)
        base_runtime = max(compute_cycles, memory_cycles)

        # 5. [Penalties]

        # A. Roundabout Penalty (재구성 패널티)
        # 형태가 128x128(정사각형)에서 멀어질수록 데이터 이동 경로가 길어짐
        shape_penalty = 0
        if R_l != 128:
            # 가로/세로 비율이 깨질수록 패널티 (경험적 가중치)
            ratio_diff = abs(math.log2(R_l / C_l))
            shape_penalty = base_runtime * (0.05 * ratio_diff) # 5% * 비율차이

        # B. Parallelism Synchronization Overhead (동기화 오버헤드)
        # 병렬 개수가 늘어나면 코어 간 통신/대기 발생
        sync_penalty = 0
        if parallel > 1:
            sync_penalty = base_runtime * 0.1 # 10% 오버헤드 가정

        final_runtime = base_runtime + shape_penalty + sync_penalty

        return int(final_runtime)


    def optimize_clusters(self):
        """
        각 클러스터별로 'Candidates' 하드웨어 조합 중
        총 런타임이 가장 짧은 'Best Config' 하나를 선정합니다.
        """
        print("\n=== [3단계] 클러스터별로 대표 최적 조합 선정 ===")

        # 클러스터 ID별로 레이어 그룹화
        clusters = {}
        for layer in self.layers:
            cid = layer['cluster_id']
            if cid not in clusters:
                clusters[cid] = []
            clusters[cid].append(layer)

        # 각 클러스터 순회
        for cid, group_layers in clusters.items():
            # 이 클러스터의 후보군 (모든 레이어가 동일한 후보군 리스트를 공유함)
            candidates = group_layers[0]['assigned_candidates']

            best_config = None
            min_total_runtime = float('inf')

            print(f"\n[Cluster {cid}] 최적화 진행")

            # 모든 후보에 대해 시뮬레이션 (Competition)
            for cand in candidates:
                total_runtime = 0
                for layer in group_layers:
                    runtime = self._estimate_runtime(layer, cand)
                    total_runtime += runtime

                # 평균 런타임 (참고용)
                avg_runtime = total_runtime / len(group_layers)

                cand_str = f"{cand['shape']} x{cand['parallel']} ({cand['flow']})"
                # print(f"   - 후보: {cand_str:<25} -> 예상 총 런타임: {total_runtime:,} cycles")

                if total_runtime < min_total_runtime:
                    min_total_runtime = total_runtime
                    best_config = cand

            # BEST 선정
            if best_config:
                # Config ID 부여 (CFG_00, CFG_01 ...)
                config_id = f"CFG_{cid:02d}"
                self.hcp_table[cid] = {
                    'config_id': config_id,
                    'best_config': best_config,
                    'total_runtime': min_total_runtime
                }

                best_str = f"{best_config['shape']} x{best_config['parallel']} ({best_config['flow']})"
                print(f"   >>> BEST: {config_id} [{best_str}] (Total: {min_total_runtime:,} cycles)")

        # 레이어 정보 업데이트 (선정된 Config ID 할당)
        for layer in self.layers:
            cid = layer['cluster_id']
            if cid in self.hcp_table:
                layer['final_config_id'] = self.hcp_table[cid]['config_id']
                layer['final_config'] = self.hcp_table[cid]['best_config']

    def generate_hcp_table(self, save_csv=True, filename="HCT.csv"):
        """ Hardware Configuration Table (HCT) 최종 출력 """

        print(f" ")
        print(f"{'ConfigID':<10} | {'Shape':<12} | {'Parallel':<8} | {'Flow':<6} | {'Target Cluster'}")
        print("-" * 60)

        for cid, info in sorted(self.hcp_table.items()):
            cfg = info['best_config']
            print(f"{info['config_id']:<10} | {str(cfg['shape']):<12} | x{cfg['parallel']:<8} | {cfg['flow']:<6} | Cluster {cid}")

        print("\n[Final Output: Hardware Configuration Table (HCT)]")
        print(f"{'LayerID':<8} | {'Modality':<8} | {'M,N,K':<15} | {'Cluster':<7} | {'Assigned Config'}")
        print("-" * 80)
        for layer in self.layers:
            dims = f"{layer['M']},{layer['N']},{layer['K']}"
            cfg_str = f"{layer['final_config_id']}"
            print(f"{layer['id']:<8} | {layer['modality']:<8} | {dims:<15} | {layer['cluster_id']:<7} | {cfg_str}")

        # CSV 파일로 저장
        if save_csv:
            print(f"\n[System] CSV 파일 저장 중: {filename}")
            try:
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['LayerID', 'Model', 'Type', 'Modality', 'M', 'N', 'K', 'ClusterID', 'ConfigID', 'Config_Shape', 'Config_Parallel', 'Config_Flow']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for layer in self.layers:
                        # Config 상세 정보 추출
                        cfg = layer.get('final_config', {})
                        shape = str(cfg.get('shape', 'N/A'))
                        parallel = cfg.get('parallel', 'N/A')
                        flow = cfg.get('flow', 'N/A')

                        writer.writerow({
                            'LayerID': layer['id'],
                            'Model': layer['model'],
                            'Type': layer.get('type', 'N/A'),
                            'Modality': layer['modality'],
                            'M': layer['M'],
                            'N': layer['N'],
                            'K': layer['K'],
                            'ClusterID': layer['cluster_id'],
                            'ConfigID': layer.get('final_config_id', 'N/A'),
                            'Config_Shape': shape,
                            'Config_Parallel': parallel,
                            'Config_Flow': flow
                        })
                print(f"[System] 저장 완료.")

                # Colab 환경이면 다운로드 실행
                if IN_COLAB:
                    print(f"[System] Colab 환경 감지됨. {filename} 다운로드를 시작합니다.")
                    files.download(filename)

            except Exception as e:
                print(f"[Error] CSV 저장 실패: {e}")

if __name__ == "__main__":

    optimizer = ClusterOptimizer(layers)
    optimizer.optimize_clusters()
    optimizer.generate_hcp_table()

