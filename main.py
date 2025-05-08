from mobvoi_tts_sdk import MobvoiTTS
import os

def text_to_speech(text: str, output_file: str = "output.mp3"):
    # 初始化TTS客户端
    # 注意：需要设置环境变量或在此处直接提供app_key和app_secret
    app_key = os.getenv("MOBVOI_APP_KEY")
    app_secret = os.getenv("MOBVOI_APP_SECRET")
    
    tts = MobvoiTTS(app_key=app_key, app_secret=app_secret)
    
    # 生成语音
    result = tts.generate(
        text=text,
        speaker="xiaoyi_meet",  # 默认说话人
        audio_type="mp3",
        speed=1.0,
        volume=1.0,
        pitch=0
    )
    
    # 保存音频文件
    with open(output_file, "wb") as f:
        f.write(result)
    
    print(f"语音文件已生成：{output_file}")

if __name__ == "__main__":
    text = "今天是2025年4月30日"
    text_to_speech(text)
