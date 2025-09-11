| 항목 | 내용 |
|------|------|
| 프로젝트명 | 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 최적화를 위한 NPU 아키텍처 설계 |
| 프로젝트 키워드 | NPU, Multi-modal, On-device, Architecture design |
| 트랙 | 연구 |
| 프로젝트 멤버 | 하정연, 최윤지, 이지현 |
| 팀지도교수 | 심재형 교수님 |
| 무엇을 만들고자 하는가 (서술형 문장으로) | 멀티모달 AI의 여러 입력 데이터 유형과 연산을 효율적으로 처리하는 최적화된 NPU 아키텍처를 설계하고 검증합니다. |
| 고객(범위를 최대한 좁혀서 지정) | • 이름: Tony <br> • 직업: 인공지능 로봇 및 자율주행차 스타트업 엔지니어 <br><br>Tony는 스타트업에서 로봇과 자율주행차에 들어갈 멀티모달 AI 모델을 개발하고 있습니다.<br>이 모델은 이미지, 텍스트, 음성, 센서 데이터를 동시에 처리해야 해서 계산량이 많습니다.<br>처음에는 클라우드 서버에서 모델을 실행했지만, 차량과 로봇의 실시간 반응 속도가 떨어져 긴급 상황에서 latency 문제가 발생했고, 안전과 사용자 경험 모두에 영향을 주었습니다.<br><br>온디바이스 실행을 시도하려고 보니, 이미지용 NPU, 텍스트용 NPU, 음성용 NPU 등 멀티모달 각각의 전용 하드웨어를 구매하면 비용과 전력 소모가 크게 증가한다는 현실적 한계에 부딪혔습니다.<br>Tony는 저전력·고효율 NPU 한 장으로 멀티모달 AI를 통합 실행할 수 있는 솔루션이 절실합니다.<br><br>Tony 외에도, AR/VR 기기 개발자, 스마트 홈 IoT 엔지니어, 드론·산업용 로봇 개발자 등 실시간 멀티모달 AI 처리와 저전력·저지연 실행이 필요한 다양한 고객들이 우리 기술의 혜택을 누릴 수 있습니다. |
| Pain Point | 1. 기존 NPU 한계: 대부분의 상용 NPU는 단일 데이터 유형(주로 CNN 이미지) 처리에 최적화되어 있어, 멀티모달 AI에 적용하기 어렵습니다. <br><br> 2. 자원 경쟁과 비효율성: 단일 NPU에서 이미지, 텍스트, 음성 등 여러 모달을 동시에 처리하면 연산 유닛과 메모리 대역폭 경쟁으로 성능 저하가 발생합니다. <br><br> 3. 온디바이스 실행의 필요성: 제한된 전력과 메모리 환경에서 복잡한 멀티모달 AI를 실행하려면, 온디바이스 환경을 고려한 멀티모달 특화 NPU 아키텍처가 필수적입니다. |
| 사용할 소프트웨어 패키지의 명칭과 핵심기능/용도 |  1. Model <br>  • OpenAI CLIP: 이미지-텍스트 멀티모달 인코더 <br>  • HuggingFace Transformers: 다양한 사전학습 모델과 데이터셋 제공 <br><br> 2. Framework <br>  • PyTorch: 딥러닝 학습 및 추론 프레임워크 <br> • TensorFlow: TPU 친화적인 딥러닝 프레임워크 <br><br> 3. NPU Simulator <br> • Scale-Sim: NPU 아키텍처 검증 및 성능 분석 <br><br> 4. 가속/최적화 <br> • ONNX Runtime: 모델 변환 및 경량화 추론 <br> • TensorRT: GPU 및 엣지 디바이스 최적화 <br> • PyTorch-XLA: 클라우드 TPU 환경에서 학습/추론 지원 <br><br> 5. 실험 관리/분석 <br> • Weights & Biases: 실험 기록 및 시각화 <br> • TensorBoard: 학습 과정 모니터링 및 시각화 |
| 사용할 소프트웨어 패키지의 명칭과 URL | 모델 : [OpenAI CLIP](https://github.com/openai/CLIP), [HuggingFace Transformers](https://huggingface.co/transformers) <br> 프레임워크 : [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/) <br> NPU 시뮬레이터 : [ONNXim](https://github.com/PSAL-POSTECH/ONNXim) <br> 가속/최적화 : [ONNX + PyTorch-XLA](https://github.com/pytorch/xla), [ONNX Runtime](https://onnxruntime.ai/), [TensorRT](https://developer.nvidia.com/tensorrt) <br> 실험 관리/분석: [Weights & Biases](https://wandb.ai/site), [TensorBoard](https://www.tensorflow.org/tensorboard) |
| 팀그라운드룰 | [GroundRule.md](./GroundRule.md) |
| 최종수정일 | 2025-09-15 |
























