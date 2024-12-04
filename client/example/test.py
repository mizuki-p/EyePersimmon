from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
import cv2
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 图像生成函数（示例使用摄像头）
def generate_frames():
    width, height = 640, 480  # 设置图像分辨率
    hue_value = 0  # 初始色相值
    while True:
        hsv_image = np.zeros((height, width, 3), dtype=np.uint8)
        hsv_image[:, :, 0] = hue_value % 180  # 色相范围: 0 - 179
        hsv_image[:, :, 1] = 255  # 饱和度设为最大值
        hsv_image[:, :, 2] = 255  # 明度设为最大值
        
        # 将 HSV 转换为 BGR（浏览器支持的格式）
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        
        # 编码为 JPEG 格式并发送
        _, buffer = cv2.imencode('.jpg', bgr_image)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')  # MJPEG 格式
        hue_value += 1  # 改变色相值以获得彩虹效果
        time.sleep(1/60)  # 控制帧率，约 30 FPS

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
