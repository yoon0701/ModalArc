| 항목 | 내용 |
|------|------|
| 프로젝트명 | 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 최적화를 위한 NPU 아키텍처 설계 |
| 프로젝트 키워드 | Multi-modal, Optimization, NPU |
| 트랙 | 연구 |
| 프로젝트 멤버 | 하정연, 최윤지, 이지현 |
| 팀지도교수 | 심재형 교수님 |
| 무엇을 만들고자 하는가 (서술형 문장으로) | 멀티모달 AI의 여러 입력 데이터 유형과 연산을 효율적으로 처리하는 최적화된 NPU 아키텍처를 설계하고 검증한다. |
| 고객(범위를 최대한 좁혀서 지정) | • 이름: Tony <br> • 직업: 인공지능 로봇 및 자율주행차 스타트업 엔지니어 <br><br>Tony는 스타트업에서 로봇과 자율주행차에 들어갈 멀티모달 AI 모델을 개발하고 있습니다.<br>이 모델은 이미지, 텍스트, 음성, 센서 데이터를 동시에 처리해야 해서 계산량이 많습니다.<br>처음에는 클라우드 서버에서 모델을 실행했지만, 차량과 로봇의 실시간 반응 속도가 떨어져 긴급 상황에서 latency 문제가 발생했고, 안전과 사용자 경험 모두에 영향을 주었습니다.<br><br>온디바이스 실행을 시도하려고 보니, 이미지용 NPU, 텍스트용 NPU, 음성용 NPU 등 멀티모달 각각의 전용 하드웨어를 구매하면 비용과 전력 소모가 크게 증가한다는 현실적 한계에 부딪혔습니다.<br>Tony는 저전력·고효율 NPU 한 장으로 멀티모달 AI를 통합 실행할 수 있는 솔루션이 절실합니다.<br><br>Tony 외에도, AR/VR 기기 개발자, 스마트 홈 IoT 엔지니어, 드론·산업용 로봇 개발자 등 실시간 멀티모달 AI 처리와 저전력·저지연 실행이 필요한 다양한 고객들이 우리 기술의 혜택을 누릴 수 있습니다. |
| Pain Point | 1. 현재 대부분의 상용 NPU는 단일 데이터 유형 처리에 최적화되어 있습니다. <br> 2. 단일 NPU에서 멀티모달 인코더 처리 시 발생하는 자원 경쟁과 비효율성이 심각합니다. <br> 3. 자원이 제한된 온디바이스 환경에서 복잡한 멀티모달 AI를 동작하려면 멀티모달 특화 NPU가 필요합니다. |
| 사용할 소프트웨어 패키지의 명칭과 핵심기능/용도 | 모델: OpenAI CLIP (이미지-텍스트 멀티모달 인코더), HuggingFace Transformers (다양한 사전학습 모델과 데이터셋 제공) <br> 프레임워크 : PyTorch (딥러닝 학습 및 추론 프레임워크), TensorFlow (TPU 친화적인 딥러닝 프레임워크) <br> NPU 시뮬레이터: ONNXim (멀티코어 NPU 시뮬레이터) <br> 가속/최적화: Google Cloud TPU + PyTorch-XLA (TPU 환경에서 PyTorch 실행 지원), ONNX Runtime (모델 변환 및 경량화 추론), TensorRT (GPU 및 엣지 디바이스용 추론 최적화) <br> 실험 관리/분석: Weights & Biases (실험 기록 및 시각화 도구), TensorBoard (학습 과정 모니터링 및 시각화) |
| 사용할 소프트웨어 패키지의 명칭과 URL | 모델 : [OpenAI CLIP](https://github.com/openai/CLIP), [HuggingFace Transformers](https://huggingface.co/transformers) <br> 프레임워크 : [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/) <br> NPU 시뮬레이터 : [ONNXim](https://github.com/PSAL-POSTECH/ONNXim) <br> 가속/최적화 : [ONNX + PyTorch-XLA](https://github.com/pytorch/xla), [ONNX Runtime](https://onnxruntime.ai/), [TensorRT](https://developer.nvidia.com/tensorrt) <br> 실험 관리/분석: [Weights & Biases](https://wandb.ai/site), [TensorBoard](https://www.tensorflow.org/tensorboard) |
| 팀그라운드룰 | [GroundRule.md](./GroundRule.md) |
| 최종수정일 | 2025-09-15 |























