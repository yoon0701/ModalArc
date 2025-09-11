| 항목 | 내용 |
|------|------|
| 프로젝트명 | 멀티모달 최적화 NPU 아키텍처 설계 |
| 프로젝트 키워드 | Multimodal, Optimization, NPU |
| 트랙 | AI/시스템 |
| 프로젝트 멤버 | 하정연, 최윤지, 이지현 |
| 팀지도교수 | 심재형 교수님 |
| 무엇을 만들고자 하는가 (서술형 문장으로) | 멀티모달 입력을 효율적으로 처리하는 최적화된 NPU 아키텍처를 설계하고 검증한다. |
| 고객(범위를 최대한 좁혀서 지정) | AI 칩 설계 기업 |
| Pain Point | 단일 NPU에서 멀티모달 인코더 처리 시 발생하는 자원 경쟁과 비효율성 |
| 사용할 소프트웨어 패키지의 명칭과 핵심기능/용도 |
|--------------------------------------|
| **모델**: OpenAI CLIP (이미지-텍스트 멀티모달 인코더), HuggingFace Transformers (다양한 사전학습 모델과 데이터셋 제공) |
| **프레임워크**: PyTorch (딥러닝 학습 및 추론 프레임워크), TensorFlow (TPU 친화적인 딥러닝 프레임워크) |
| **가속/최적화**: Google Cloud TPU + PyTorch-XLA (TPU 환경에서 PyTorch 실행 지원), ONNX Runtime (모델 변환 및 경량화 추론), TensorRT (GPU 및 엣지 디바이스용 추론 최적화) |
| **실험 관리/분석**: Weights & Biases (실험 기록 및 시각화 도구), TensorBoard (학습 과정 모니터링 및 시각화) |
| 사용할 소프트웨어 패키지의 명칭과 URL |
|--------------------------------------|
| **모델**: [OpenAI CLIP](https://github.com/openai/CLIP), [HuggingFace Transformers](https://huggingface.co/transformers) |
| **프레임워크**: [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/) |
| **가속/최적화**: [Google Cloud TPU + PyTorch-XLA](https://github.com/pytorch/xla), [ONNX Runtime](https://onnxruntime.ai/), [TensorRT](https://developer.nvidia.com/tensorrt) |
| **실험 관리/분석**: [Weights & Biases](https://wandb.ai/site), [TensorBoard](https://www.tensorflow.org/tensorboard) |
| 팀그라운드룰 | [GroundRule.md](./GroundRule.md) |
| 최종수정일 | 2025-09-15 |

