from EP.types import ViewDataFlow, ViewMode
from .base_env import BaseEnv
import numpy as np
import cv2
import time
from typing import Callable

def generate_image(alive: Callable[[], bool]):
    width, height = 640, 480
    hue_value = 0
    
    while alive():
        hsv_image = np.zeros((height, width, 3), np.uint8)
        hsv_image[:, :, 0] = hue_value % 180
        hsv_image[:, :, 1] = 255
        hsv_image[:, :, 2] = 255
        
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        _, buffer = cv2.imencode('.jpg', bgr_image)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')   
        
        hue_value += 1
        time.sleep(1/60)



def get_env():
    return BaseEnv(
        env_name='我也不知道这个环境应该叫什么名字，总之它是为了测试直接在服务端获取图片然后串流到流媒体服务器上，然后网页访问的',
        scene_name="写下这行名称的时候，我饿了",
        
        nop_code=None,
        observation_captor=lambda : None,
        action_executor=lambda _ : None,
        check_init=lambda : True,
        reset_env=lambda : None,
        
        view_mode=ViewMode.Transfer,
        view_data_flow=ViewDataFlow.Active,
        video_pusher=generate_image,
    )