import pandas as pd
import os
from analyzer import ModalityStrategist
from clusterer import PatternClusterer
from optimizer import ClusterOptimizer

def run_compiler():
    # 1. [Analyzer] 로그 파싱 및 스케줄러 1단계 수행
    analyzer = ModalityStrategist("output.log")
    analyzer.upload_and_parse_log()
    analyzer.aware_modality()

    # 2. [Clusterer] 스케줄러 2단계 수행
    clusterer = PatternClusterer(analyzer.layers)
    clusterer.cluster_layers_and_assign_config(n_clusters=4)

    # 3. [Optimizer] 스케줄러 3단계 최적화 수행
    optimizer = ClusterOptimizer(analyzer.layers)
    optimizer.optimize_clusters()

    # 최종 HCT 결과 출력 및 csv 파일 생성
    optimizer.generate_hcp_table()

if __name__ == "__main__":
    run_compiler()
