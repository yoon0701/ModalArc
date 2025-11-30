# 온디바이스 환경에서 이미지-텍스트 기반 멀티모달 AI 추론을 위한 NPU 하드웨어 가속기 설계
---
## 🦾 Team ModalArc
이화여자대학교 캡스톤디자인과창업프로젝트 연구 팀<br>
하정연, 최윤지, 이지현

본 연구는 **전력과 자원이 제한된 On-Device 환경에서, 멀티모달 AI를 효율적으로 추론하기 위한 차세대 NPU 하드웨어 가속기 및 스케줄러 설계**를 제안합니다. 기존 NPU 아키텍처가 가진 데이터 이질성(Data Heterogeneity) 및 비효율적 하드웨어 재구성 문제를 해결하기 위해, 컴파일 타임에 모달리티 특성을 반영하여 최적의 하드웨어 조합을 결정하는 **Modality-Aware Dynamic Scheduler**를 구현합니다. 

ONNXim 시뮬레이터를 기반으로 구현되었으며, 대표적인 이미지-텍스트 멀티모달 모델인 CLIP을 통해 제안된 아키텍처의 성능(Latency, Energy efficiency, Utilization) 향상을 입증합니다.



## 🔑 Research Keywords
`NPU Architecture design` | `On-device AI` | `Multimodal AI` | `Scheduler`

## 💡 Background

**멀티모달 AI의 부상과 온디바이스 컴퓨팅의 중요성**<br>
최근 Google, Tesla와 같은 글로벌 기업들이 자율주행, 로봇, 스마트 디바이스 등 다양한 분야에서 멀티모달 AI를 핵심 기술로 채택하며 그 수요가 급증하고 있습니다. 멀티모달 AI는 이미지, 텍스트, 음성, 액션 등 여러 종류의 데이터를 실시간으로 함께 처리하여 기존 AI 모델보다 훨씬 더 풍부한 정보를 이해하고 복합적인 추론을 수행합니다. <br><br>하지만 복잡한 멀티모달 AI 모델을 클라우드 서버에만 의존해 실행할 경우, 지연 시간 증가, 운영 비용 부담, 네트워크 의존성 등의 문제가 불가피합니다. 이러한 멀티모달 AI 모델을 클라우드 서버에 의존하지 않고, 저전력, 저지연성이 필수적인 온디바이스 환경에서 직접 실행하는 것이 중요한 과제로 떠오르고 있습니다.<br><br>

**기존 NPU의 한계 및 기존 하드웨어 동적 재구성 연구의 한계**<br>
1. 기존 NPU의 한계: **모달리티별 자원 불균형 (Resource Imbalance)** <br>
기존의 고정된 NPU는 주로 이미지 처리에 편향되어 있습니다. 따라서 텍스트, 음성, 액션 모델과 같이 데이터 형태와 연산 패턴이 상이한 작업을 동시에 처리할 때, 심각한 자원 활용률 저하와 전력 비효율성이 발생합니다.

2. 기존 하드웨어 동적 재구성 연구의 한계<br>
기존 하드웨어 동적 재구성 연구의 스케줄링은 개별 레이어의 구조 및 차원 정보만으로 지역적 최적화를 수행하여 모델의 Global Context을 놓치고, 레이어가 바뀔 때마다 하드웨어 구조를 빈번하게 변경하게 되어 재구성 오버헤드를 발생시킵니다.
또한 런타임에 최적의 하드웨어 조합을 탐색하고 결정하여, **스케줄링 자체의 전력 및 시간 오버헤드**가 커 온디바이스 환경에 부적합합니다. <br><br>

이러한 한계들 때문에 기존 NPU에 멀티모달 AI 모델을 그대로 적용하면 성능 저하, 전력 소모 증가 등 여러 비효율이 발생합니다. <br>
따라서 온디바이스라는 환경을 고려함과 동시에 멀티모달 AI에 특화된 **새로운 NPU 아키텍처 연구**가 필수적입니다. 

## 🎯 Research Topic and Methodology

### 1. 선행 연구 분석 및 문제 정의
* 우선 하드웨어 동적 재구성과 관련된 선행 연구 논문들을 심층적으로 분석하고, 기존 연구가 충분히 고려하지 못한 문제들을 파악합니다.
* GitHub에 오픈 소스로 공개된 POSTECH의 ONNXim NPU 기본 시뮬레이터를 사용하여, 이미지와 텍스트를 조합한 소규모의 대표적인 멀티모달 모델 OPEN AI의 CLIP을 실행합니다. 이때 메모리 접근 패턴, 연산량, 지연 시간 등의 데이터를 프로파일링하여, 성능 병목 현상과 비효율성을 직접 확인하고, 이를 개선하기 위한 설계의 논리적 근거를 마련합니다.

### 2. Key Methodology
본 연구는 "지능적인 판단은 컴파일 타임에, 실행은 가볍게"라는 철학을 바탕으로 **3단계로 구성된 Knowledge-Guided Mapper**를 제안합니다.

* **Step 1: Modality-Awareness**<br> 
  모달리티의 종류를 사전에 인지하여, 각 모달리티에 적합한 하드웨어 탐색 가이드라인을 수립합니다. 
* **Step 2: Clustering-based Optimization**<br> 
  유사한 연산 패턴을 가진 레이어들을 Clustering하여, 하드웨어 동적 재구성 횟수를 최소화하고 탐색 효율을 높입니다.
* **Step 3 : Optimal Hardware Configuration**<br> 
  클러스터 별로 최적의 하드웨어 설정을 도출하여, HCT (Hardware Configuration Table)을 생성합니다.
* **Zero-Overhead Runtime**<br> 
  생성된 정적 테이블을 런타임에 Look-up하여 스케줄링 비용을 최소화합니다.

(자세한 알고리즘 및 실험 결과는 추후 공개될 논문을 참고해 주세요.)

### 3. Implementation
* **Language**: Python
* **Target Model**: OpenAI CLIP (ViT-B/32 + Transformer)
* **NPU (TPU v4) Simulator** : Postech ONNXim
* **Evaluation**: Latency, Energy Efficiency, PE Utilization <br> 
* **Goal**: 제안한 아키텍쳐가 기존 NPU 아키텍처 대비 성능과 효율을 얼마나 개선하는지 정량적으로 평가합니다. 

## 🙋🏻‍♀️ Project Plan
* 2025년 9월: 선행 연구 분석 및 문제 정의
* 2025년 10월: 프로파일링 실험 통해 설계 주체 구체화
* 2025년 겨울: Modality-Aware Dynamic Scheduler 구현 및 성능 측정 후 아키텍처 최적화
* 2026년 봄: 학회 논문 작성 및 발표
