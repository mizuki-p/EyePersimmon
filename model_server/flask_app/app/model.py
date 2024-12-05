from transformers import BlipProcessor, BlipForImageTextRetrieval
from PIL import Image

# import asyncio


class BlipInference:
    def __init__(self, model_path, processor_path):
        """加载模型和处理器"""
        self.processor = BlipProcessor.from_pretrained(processor_path)
        self.model = BlipForImageTextRetrieval.from_pretrained(model_path).to("cuda")
        print("Model and processor loaded successfully!")

    def infer(self, observation, instruction):
        """推理逻辑"""
        raw_image = Image.open(observation)
        inputs = self.processor(raw_image, instruction, return_tensors="pt").to("cuda")
        print(f"Performing inference ......")
        itm_scores = self.model(**inputs)[0]
        res = itm_scores.tolist()[0]  # 转为 Python 列表
        return res


# 初始化模型
inference_engine = BlipInference(
    model_path="/data/nvme2/dky/lc/EyePersimmon/blip-itm-base-coco",
    processor_path="/data/nvme2/dky/lc/EyePersimmon/blip-itm-base-coco",
)

# # 测试推理
# observation = "/data/nvme2/dky/lc/image_1.png"
# instruction = "a man is talking to someone."
# res = inference_engine.infer(observation, instruction)
# print(res)
