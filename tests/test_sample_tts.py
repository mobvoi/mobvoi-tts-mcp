
# coding=utf-8
import time
import hashlib
import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

timestamp = str(int(time.time()))
appkey = os.getenv("APP_KEY")
secret = os.getenv("APP_SECRET")

message = '+'.join([appkey, secret, timestamp])

m = hashlib.md5()
m.update(message.encode("utf8"))
signature = m.hexdigest()

http_url = 'https://open.mobvoi.com/api/tts/v1'

def sample_tts():
    data = {
        'text': '出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。',
        'speaker': 'galaxy_fastv7||||eb538df318ecd1ce94ff5480132671b6',
        'audio_type': 'mp3',
        'speed': 1.0,
        'gen_srt': False, # 是否生成srt字幕文件，默认不开启。如果开启生成字幕，需要额外计费。生成好的srt文件地址将通过response header中的srt_address字段返回。
        'appkey': appkey,
        'timestamp': timestamp,
    'signature': signature
    }
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=http_url, headers=headers, data=json.dumps(data))
        content = response.content

        with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), "sample.mp3"), "wb") as f:
            f.write(content)
    except Exception as e:
        print("error: {0}".format(e))
        
if __name__ == "__main__":
    sample_tts()