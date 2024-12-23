from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor,MllamaForConditionalGeneration
from qwen_vl_utils import process_vision_info
import torch
from PIL import Image

class QwenInference:
    def __init__(self,model_path,processor_path):
        self.model=Qwen2VLForConditionalGeneration.from_pretrained(model_path,torch_dtype=torch.float16, device_map="auto" )
        self.processor=AutoProcessor.from_pretrained(processor_path)
    
    def infer(self,image,system_prompt,question):
        messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': [
            {'type': 'image', 'image':image},
            {'type': 'text', 'text': question}
        ]}
    ]
        
        # image = Image.open(image_path)
        # Preparation for inference
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            images=image_inputs,
            text=text,
            # videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        # device = torch.device("cuda:5")
        inputs = inputs.to("cuda")
        generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        # save_log(f'<||Response||>: {res}')
        return output_text

inference_engine = QwenInference(
    model_path="/home/zhangshuai/data/boundless/EyePersimmon/pretrained_models/Qwen2-VL-7B-Instruct/",
    processor_path="/home/zhangshuai/data/boundless/EyePersimmon/pretrained_models/Qwen2-VL-7B-Instruct",
)
# # 测试推理
# observation = Image.open("/home/zhangshuai/data/boundless/demo.jpeg")
# observation=observation.resize((1024,1024))
# # instruction1="When I ask you to do something, you are supposed to give me Python code that is needed to "
# system_prompt="You are an assistant helping me with the AirSim simulator for drone or car.When I ask you to do something, you are supposed to give me Python code that is needed to achieve that task using AirSim and then an explanation of what that code does. You are only allowed to use the functions I have defined for you.You are not to use any other hypothetical functions that you think might exist.You can use simple Python functions from libraries such as math and numpy."
# instruction = " describe the image "

# res = inference_engine.infer(observation,system_prompt,instruction)
# print(res)


