# 🦾 Team 38 ModalArc 

| 항목 | 내용 |
|------|------|
| 프로젝트명 | 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 실행 최적화를 위한 NPU 아키텍처 설계
| 프로젝트 키워드 | NPU Architecture design, Multi-modal AI, On-device |
| 트랙 | 연구 |
| 프로젝트 멤버 | 하정연, 최윤지, 이지현 |
| 팀지도교수 | 심재형 교수님 |
| 무엇을 만들고자 하는가 (서술형 문장으로) | 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 모델을 저전력·저지연·고성능으로 실행하기 위해, 데이터 흐름 최적화, 이질적인 자원 관리, 멀티모달 융합 가속, 온칩 메모리 관리 등 핵심 요소를 포함한 멀티모달 특화 NPU 아키텍처를 제안합니다. |
| 고객(범위를 최대한 좁혀서 지정) | 인공지능 로봇 엔지니어, 자율주행차 엔지니어, IoT 엔지니어, 웨어러블 디바이스 연구자, 드론·산업용 로봇 개발자 등 실시간 멀티모달 AI 처리와 저전력·저지연·고성능 실행이 필요한 다양한 고객들이 기술 혜택을 누릴 수 있습니다. <br><br> • 이름: Tony <br> • 직업: 인공지능 로봇 스타트업 엔지니어 <br><br> Tony는 인공지능 휴머노이드 로봇에서 실행할 멀티모달 AI 모델을 개발하고 있습니다. 이 모델은 이미지, 텍스트, 음성, 액션 데이터를 동시에 처리해야 해서 계산량이 많습니다. 초기에는 클라우드 서버에서 모델을 실행했지만, 로봇의 실시간 반응 속도가 떨어져 긴급 상황에서 latency 문제가 발생했고, 안전과 사용자 경험 모두에 영향을 주었습니다.<br><br> 온디바이스 실행을 시도하려고 보니, 이미지용 NPU, 텍스트용 NPU, 음성용 NPU 등 각 모달별 전용 하드웨어를 구매하면 비용과 전력 소모가 크게 증가한다는 현실적 한계에 부딪혔습니다. Tony는 저전력·저지연·고성능 NPU 한 장으로 멀티모달 AI를 통합 실행할 수 있는 솔루션이 절실합니다. |
| Pain Point | 1. 기존 NPU 한계<br>  현재 시장에 출시된 상용 NPU의 대부분은 단일 데이터 타입(주로 이미지) 처리에 최적화되어 있으며, CNN 기반 연산 가속에 초점을 맞추고 있습니다. 그러나 멀티모달 AI는 이미지, 텍스트 등 이질적인 데이터를 동시에 다루어야 하므로 기존 구조에서는 다음과 같은 문제가 발생합니다. <br><br> • Data Heterogeneity으로 인한 비효율성: 각 모달리티는 서로 다른 데이터 구조와 연산 패턴을 가지고 있습니다. 예를 들어, 이미지 처리는 주로 컨볼루션 연산(CNN) 에 집중되어 있고, 텍스트 처리는 트랜스포머 기반의 Attention 연산에 특화되어 있습니다. 기존 NPU는 이러한 이질적인 데이터를 동시에 처리하는 데 적합하지 않아, 하드웨어 자원 활용률이 낮아지고 연산 효율이 급격히 떨어집니다. <br> • Memory Bottleneck 문제: 멀티모달 모델은 여러 데이터 스트림을 융합하는 과정에서 서로 다른 메모리 영역에 분산된 데이터를 동시에 불러와야 합니다. 이때 한정된 메모리 대역폭을 두고 연산 유닛 간 경쟁(Contestion)이 발생하며, 이는 시스템 전반의 성능 저하를 유발하는 핵심 원인이 됩니다. <br><br> 2. 온디바이스 실행의 필요성 <br> 복잡한 멀티모달 AI 모델을 클라우드 서버에만 의존해 실행할 경우, 지연 및 운영 비용, 네트워크 의존성 문제가 불가피합니다. 제한된 전력과 메모리 환경에서 복잡한 멀티모달 AI를 실행하려면, 온디바이스 환경을 고려한 멀티모달 특화 NPU 아키텍처가 필수적입니다. |
| 사용할 소프트웨어 패키지의 명칭과 핵심기능/용도 |  1. Model <br>  • OpenAI CLIP: 이미지-텍스트 멀티모달 인코더 <br>  • HuggingFace Transformers: 다양한 사전학습 모델과 데이터셋 제공 <br><br> 2. Framework <br>  • PyTorch: 딥러닝 학습 및 추론 프레임워크 <br> • TensorFlow: TPU 친화적인 딥러닝 프레임워크 <br><br> 3. NPU Simulator <br> • POSTECH ONNXim: NPU 아키텍처 검증 및 성능 분석 <br><br> 4. 가속/최적화 <br> • ONNX Runtime: 모델 변환 및 경량화 추론 <br> • TensorRT: GPU 및 엣지 디바이스 최적화 <br> • PyTorch-XLA: 클라우드 TPU 환경에서 학습/추론 지원 <br><br> 5. 실험 관리/분석 <br> • Weights & Biases: 실험 기록 및 시각화 <br> • TensorBoard: 학습 과정 모니터링 및 시각화 |
| 사용할 소프트웨어 패키지의 명칭과 URL |  • OpenAI CLIP: https://github.com/openai/CLIP <br> • HuggingFace Transformers: https://huggingface.co/transformers <br> • PyTorch: https://pytorch.org/ <br> • TensorFlow: https://www.tensorflow.org <br> • ONNXim: https://github.com/PSAL-POSTECH/ONNXim <br> • ONNX + PyTorch-XLA:https://github.com/pytorch/xla <br> • ONNX Runtime: https://onnxruntime.ai/ <br> • TensorRT: https://developer.nvidia.com/tensorrt <br> • Weights & Biases: https://wandb.ai/site <br> • TensorBoard: https://www.tensorflow.org/tensorboard |
| 팀그라운드룰 | https://github.com/yoon0701/ModalArc/blob/main/GroundRule.md |
| 최종수정일 | 2025-09-16 |



































