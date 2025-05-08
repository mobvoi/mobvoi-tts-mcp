import os, sys
from datetime import datetime
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx
from dotenv import load_dotenv

from mobvoi_tts_sdk import MobvoiTTS

load_dotenv()

def test_voice_clone():
    custom_client = httpx.Client(
        timeout=10
    )
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = custom_client
    )
    
    speaker = client.async_voice_clone_local(
        audio_file_path = "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav"
    )
    print(f"speaker: {speaker}")
    
async def aysnc_test_voice_clone():
    async_custom_client = httpx.AsyncClient(
        timeout=10
    )
    
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = async_custom_client
    )
    
    speaker = await client.async_voice_clone_local(
        audio_file_path = "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav"
    )
    print(f"speaker: {speaker}")
        
async def test_voice_clone_concurrency():
    async_custom_client = httpx.AsyncClient(
        timeout=30  # increase timeout to adapt to concurrent requests
    )
    
    client = MobvoiTTS(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        httpx_client = async_custom_client
    )
    
    # test local audio list
    test_local_paths = [
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
        "/Users/kk/workspace/mobvoi_tts-mcp/tests/taiyi.wav",
    ]
    
    start_time = datetime.now()
    
    # create multiple concurrent tasks
    tasks = [client.async_voice_clone_local(audio_file_path=path) for path in test_local_paths]
    
    # execute all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # print the results
    print(f"\nConcurrency test results:")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Request count: {len(test_local_paths)}")
    print(f"Average response time: {duration/len(test_local_paths):.2f} seconds")
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Request {i+1} failed: {str(result)}")
        else:
            print(f"Request {i+1} success: speaker={result}")
    
    await async_custom_client.aclose()

if __name__ == "__main__":
    # asyncio.run(aysnc_test_voice_clone())
    asyncio.run(test_voice_clone_concurrency())