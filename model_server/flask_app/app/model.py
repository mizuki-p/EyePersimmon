import numpy as np

def load_model():
    """加载机器学习模型"""
    print("Model loaded successfully!")
    return "mock_model"  

def model_inference(observation, instruction):
    """模拟模型推理"""
    
    print(f"Performing inference ......")
    return list(np.random.rand(3))# action_vector
