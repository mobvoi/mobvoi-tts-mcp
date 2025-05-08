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

print(f"appkey: {appkey}")
print(f"secret: {secret}")
print(f"timestamp: {timestamp}")
message = '+'.join([appkey, secret, timestamp])

m = hashlib.md5()
m.update(message.encode("utf8"))
signature = m.hexdigest()
print(f"signature: {signature}")

file_path = '/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav'
wavUri_path = 'https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav'
file_text = '对，这就是我，万人景仰的太乙真人。'

http_url = 'https://open.mobvoi.com/clone'

def voice_clone():
    import requests

    url = 'https://open.mobvoi.com/clone'

    data = {
        'appKey': appkey,
        'signature': signature,
        'timestamp': timestamp,
        'wavUri': wavUri_path,
    }

    # 文件字段
    # files = {
    #     # 'file': open('/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav', 'rb')
    # }

    try:
        # 发起 POST 请求
        # response = requests.post(url, data=data, files=files)
        response = requests.post(url, data=data)
        # 输出响应
        print("状态码:", response.status_code)
        print("响应内容:", response.text)
        print("speaker:", response.json()['speaker'])
    except Exception as e:
        print("error: {0}".format(e))

if __name__ == "__main__":
    voice_clone()
