import os, sys
from datetime import datetime
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx
from dotenv import load_dotenv

from mobvoi_tts_sdk import MobvoiTTS

load_dotenv()

def main():
    custom_client = httpx.Client(
        timeout=10
    )
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = custom_client
    )
    
    text = '出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。'
    output_dir = os.path.dirname(os.path.abspath("__file__"))
    
    content = client.speech_generate(
        text=text,
        speaker="mercury_yunxi_24k",
    )
    
    output_file_path = os.path.dirname(os.path.abspath("__file__")) + f"/tests/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    print(f"output_file_path: {output_file_path}")
    with open(output_file_path, "wb") as f:
        f.write(content)
        
async def async_main():
    custom_client = httpx.Client(
        timeout=10
    )
    async_custom_client = httpx.AsyncClient(
        timeout=10
    )
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = async_custom_client
    )
    
    text = '出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。'
    output_dir = os.path.dirname(os.path.abspath("__file__"))
    
    content = await client.async_speech_generate(
        text=text,
    )
    
    output_file_path = os.path.dirname(os.path.abspath("__file__")) + f"/tests/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    print(f"output_file_path: {output_file_path}")
    with open(output_file_path, "wb") as f:
        f.write(content)
        
async def test_generate_concurrency():
    async_custom_client = httpx.AsyncClient(
        timeout=30  # 增加超时时间以适应并发请求
    )
    
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = async_custom_client
    )
    
    # test text list
    # interface request frequency limit: 5 times/second
    test_texts = [
        "出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。",
        "出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。",
        "出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。",
        "出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。",
        "出门问问成立于2012年，是一家以语音交互和软硬结合为核心的人工智能公司，为全球40多个国家和地区的消费者、企业提供人工智能产品和服务。",
    ]
    
    start_time = datetime.now()
    
    # create multiple concurrent tasks
    tasks = []
    for text in test_texts:
        task = client.async_speech_generate(text=text)
        tasks.append(task)
    
    # execute all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # print the results
    print(f"\nConcurrency test results:")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Request count: {len(test_texts)}")
    print(f"Average response time: {duration/len(test_texts):.2f} seconds")
    
    # save the generated audio file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Request {i+1} failed: {str(result)}")
        else:
            output_file_path = os.path.join(output_dir, f"concurrent_test_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
            try:
                with open(output_file_path, "wb") as f:
                    f.write(result)
                print(f"Request {i+1} success: saved to {output_file_path}")
            except Exception as e:
                print(f"Request {i+1} success but save failed: {str(e)}")
    
    await async_custom_client.aclose()

if __name__ == "__main__":
    main()
    # asyncio.run(main())
    # asyncio.run(test_generate_concurrency())