# 🦾 Team 38 ModalArc 

| 항목 | 내용 |
|------|------|
| 프로젝트명 | 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 추론을 위한 NPU 하드웨어 가속기 설계
| 프로젝트 키워드 | NPU Architecture design, Multi-modal AI, On-device, Scheduler |
| 트랙 | 연구 |
| 프로젝트 멤버 | 하정연, 최윤지, 이지현 |
| 팀지도교수 | 심재형 교수님 |
| 무엇을 만들고자 하는가 (서술형 문장으로) | 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 모델을 저전력·저지연·고성능으로 추론하기 위해, Modality-Aware Dynamic Scheduler를 핵심으로 하는 NPU 아키텍처를 제안합니다. 이 아키텍처는 연산의 모달리티별 특성을 인지하고, Systolic Array의 논리적 Shape · Dataflow · 메모리 계층 구조 · 병렬 처리 자원 등 NPU 하드웨어를 동적으로 재구성하는 지능형 스케줄러를 구현합니다. |
| 고객(범위를 최대한 좁혀서 지정) | 본 기술은 멀티모달 AI를 실시간으로 처리하면서도 저전력·저지연·고성능 특성이 요구되는 다양한 분야에 적용 가능합니다. 특히 인공지능 휴머노이드 로봇, 자율주행차, IoT, 웨어러블, 드론, 산업용 로봇 분야의 엔지니어와 연구자가 직접적인 혜택을 누릴 수 있습니다. <br><br> <페르소나> <br> • 이름: Tony <br> • 직업: 인공지능 로봇 스타트업 엔지니어 <br><br> Tony는 인공지능 휴머노이드 로봇에서 실행할 멀티모달 AI 모델을 개발하고 있습니다. 이 모델은 이미지, 텍스트, 음성, 액션 데이터를 동시에 처리해야 해서 계산량이 많습니다. 초기에는 클라우드 서버에서 모델을 실행했지만, 로봇의 실시간 반응 속도가 떨어져 긴급 상황에서 latency 문제가 발생했고, 안전과 사용자 경험 모두에 영향을 주었습니다.<br><br> 온디바이스 실행을 시도하려고 보니, 이미지용 NPU, 텍스트용 NPU, 음성용 NPU 등 각 모달리티별 전용 하드웨어를 구매하면 비용과 전력 소모가 크게 증가한다는 현실적 한계에 부딪혔습니다. Tony는 저전력·저지연·고성능 NPU 한 장으로 멀티모달 AI를 통합 실행할 수 있는 솔루션이 절실합니다. |
| Pain Point | **1. 기존 NPU의 한계** <br> 현재 상용 NPU는 대부분 이미지 중심 CNN 연산에 최적화되어 있어, 멀티모달 AI의 이미지·텍스트 등 이질적인 데이터를 동시에 처리하기 어렵습니다. 이러한 **Data Heterogeneity(데이터 이질성)** 문제로 인해 자원 활용률 저하와 연산 비효율성이 발생합니다. 또한 고정된 메모리 정책으로 이질적인 모달리티 데이터를 불러오는 과정에서 **Memory Bottleneck(메모리 병목)** 문제가 나타나 latency 증가와 전력 낭비 등 성능 저하를 유발합니다. <br><br> **2. 온디바이스 실행의 필요성** <br> 복잡한 멀티모달 AI 모델을 클라우드 서버에만 의존해 실행할 경우, 지연 시간 증가, 운영 비용 부담, 네트워크 의존성 등의 문제가 불가피합니다. 따라서 제한된 전력 및 메모리 자원 환경에서도 효율적으로 동작할 수 있도록, 온디바이스 환경을 고려한 멀티모달 특화 NPU 아키텍처가 필수적입니다. |
| 사용할 소프트웨어 패키지의 명칭과 핵심기능/용도 |  1. Model <br>  • OpenAI CLIP: 이미지-텍스트 멀티모달 인코더 <br>  • HuggingFace Transformers: CLIP 포함 다양한 사전학습 모델과 데이터셋 제공 <br><br> 2. Framework <br>  • PyTorch: 딥러닝 학습과 추론 프레임워크 및 ONNX 변환 <br><br> 3. NPU Simulator <br> • POSTECH ONNXim: NPU 아키텍처 검증 및 성능 분석 <br><br> 4. 가속/최적화 <br> • ONNX Runtime: 모델 변환 및 경량화 추론 <br> • TensorRT: GPU 및 엣지 디바이스 최적화 <br><br> 5. 실험 관리/분석 <br> • Weights & Biases: 실험 기록 및 시각화 <br> • TensorBoard: 학습 과정 모니터링 및 시각화 |
| 사용할 소프트웨어 패키지의 명칭과 URL |  • OpenAI CLIP: https://github.com/openai/CLIP <br> • HuggingFace Transformers: https://huggingface.co/transformers <br> • PyTorch: https://pytorch.org/ <br> • ONNXim: https://github.com/PSAL-POSTECH/ONNXim <br> • ONNX Runtime: https://onnxruntime.ai/ <br> • TensorRT: https://developer.nvidia.com/tensorrt <br> • Weights & Biases: https://wandb.ai/site <br> • TensorBoard: https://www.tensorflow.org/tensorboard |
| 팀그라운드룰 | https://github.com/yoon0701/ModalArc/blob/main/GroundRule.md |
| 최종수정일 | 2025-11-13 |












































