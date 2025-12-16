import numpy as np
import re
import os


# Colab 환경 여부 확인 및 다운로드 함수
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False


# 로그 읽고 파싱
# --- [Step 1] 모달리티를 인식하여 전략 수립하는 클래스 ---
class ModalityStrategist:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.layers = []

    def upload_and_parse_log(self):
        """
        로컬 파일을 업로드 받아 파싱합니다.
        """

        # 1. 파일 업로드
        if IN_COLAB:
            if not os.path.exists(self.log_file_path):
                print(f"[System] '{self.log_file_path}' 파일이 없습니다. 업로드를 요청합니다.")
                uploaded = files.upload()

                if uploaded:
                    self.log_file_path = list(uploaded.keys())[0]
                    print(f"[System] 파일 업로드 완료: {self.log_file_path}")
                else:
                    print("[Warning] 파일 업로드가 취소되었습니다. 기본 파일명을 사용합니다.")
            else:
                print(f"[System] 기존 파일 '{self.log_file_path}'을 사용합니다.")
        else:
            print(f"[System] 로컬 환경입니다. '{self.log_file_path}' 파일을 찾습니다.")

        # 2. 파일 파싱
        self.layers = []
        try:
            with open(self.log_file_path, "r") as f:
                print(f"[System] 로그 파싱 시작...")
                for line in f:
                    try:
                        if line.strip().startswith("{") and "model" in line:
                             layer_data = eval(line.strip())
                             self.layers.append(layer_data)
                    except Exception as e:
                        continue

            if not self.layers:
                print("[Error] 파싱된 데이터가 없습니다. 로그 파일 형식을 확인해주세요.")
            else:
                print(f"[System] 총 {len(self.layers)}개 레이어 데이터 파싱 완료.\n")

        except FileNotFoundError:
            print(f"[Error] 파일을 찾을 수 없습니다: {self.log_file_path}")


    def aware_modality(self):
        """ [1단계] 모달리티 인식 및 전체 전략 수립 (Shape, Flow, Parallel) """
        print("=== [1단계] 모달리티 인식 및 전략 수립 ===")
        for layer in self.layers:
            strategy = {}
            if 'image' in layer['model']:
                layer['modality'] = 'Image'
                strategy = {
                    'shape': "Balanced/Wide",
                    'flow': "WS preferred (Weight Reuse)",
                    'parallel': "Single (1-way)"
                }
            elif 'text' in layer['model']:
                layer['modality'] = 'Text'
                strategy = {
                    'shape': "Narrow/Long",
                    'flow': "OS preferred (Accumulation)",
                    'parallel': "Parallel (2-way/4-way)"
                }
            else:
                layer['modality'] = 'Unknown'
                strategy = {'shape': "General", 'flow': "Hybrid", 'parallel': "Adaptive"}

            layer['guide'] = strategy

            print(f"Layer {layer['id']} ({layer['model']} - {layer['type']}) -> Modality: {layer['modality']}")
            print(f"   ㄴ Guide: Shape[{strategy['shape']}], Flow[{strategy['flow']}], Parallel[{strategy['parallel']}]")

        print("=== 1단계 완료 ===\n")

        return self.layers


if __name__ == "__main__":

    # 스케줄러 1단계 실행
    analyzer = ModalityStrategist("output.log")

    analyzer.upload_and_parse_log()
    analyzer.aware_modality()
