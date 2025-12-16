import torch
import clip
from PIL import Image


# ONNX 변환을 위해 텍스트 인코더를 감싸는 래퍼 클래스
class TextEncoderWrapper(torch.nn.Module):
    def __init__(self, clip_model):
        super().__init__()
        self.clip_model = clip_model

    def forward(self, text):
        return self.clip_model.encode_text(text)


def convert_clip_to_onnx(device):
    """
    사전 학습된 CLIP 모델을 ONNX 형식으로 변환합니다.
    """
    # 1. CLIP 모델 로드
    model, _ = clip.load("ViT-B/32", device=device, jit=False)
    model.eval()
    print("CLIP 모델 로딩 완료.")

    # 2. 이미지 인코더 ONNX 변환
    image_encoder = model.visual
    dummy_image_input = torch.randn(1, 3, 224, 224).to(device)
    image_output_path = "clip_image_encoder.onnx"

    torch.onnx.export(
        image_encoder,
        dummy_image_input,
        image_output_path,
        input_names=['image_input'],
        output_names=['image_features'],
        opset_version=14,
        dynamic_axes={'image_input': {0: 'batch_size'}, 'image_features': {0: 'batch_size'}}
    )
    print(f"이미지 인코더가 '{image_output_path}' 파일로 저장되었습니다.")

    # 3. 텍스트 인코더 ONNX 변환
    text_encoder_wrapper = TextEncoderWrapper(model)
    dummy_text_input = clip.tokenize(["a photo of a cat"]).to(device)
    text_output_path = "clip_text_encoder.onnx"

    torch.onnx.export(
        text_encoder_wrapper,
        dummy_text_input,
        text_output_path,
        input_names=['text_input'],
        output_names=['text_features'],
        opset_version=14,
        dynamic_axes={'text_input': {0: 'batch_size'}, 'text_features': {0: 'batch_size'}}
    )
    print(f"텍스트 인코더가 '{text_output_path}' 파일로 저장되었습니다.")


if __name__ == "__main__":
    selected_device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"ONNX 변환에 사용될 장치: {selected_device.upper()}")
    convert_clip_to_onnx(selected_device)
