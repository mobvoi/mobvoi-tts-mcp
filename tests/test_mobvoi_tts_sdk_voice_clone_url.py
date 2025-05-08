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
    
    speaker = client.async_voice_clone_url(
        wav_uri = "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav"
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
    
    speaker = await client.async_voice_clone_url(
        wav_uri = "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav"
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
    
    # test audio url list
    test_urls = [
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
        "https://tc-nj-backend-pub-cdn.mobvoi.com/subtitles/wav/9e5d439e0e9142966037fb80fe9e0d8e.wav",
    ]
    
    start_time = datetime.now()
    
    # create multiple concurrent tasks
    tasks = [client.async_voice_clone_url(wav_uri=url) for url in test_urls]
    
    # execute all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # print the results
    print(f"\nConcurrency test results:")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Request count: {len(test_urls)}")
    print(f"Average response time: {duration/len(test_urls):.2f} seconds")
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Request {i+1} failed: {str(result)}")
        else:
            print(f"Request {i+1} success: speaker={result}")
    
    await async_custom_client.aclose()

if __name__ == "__main__":
    # asyncio.run(aysnc_test_voice_clone())
    asyncio.run(test_voice_clone_concurrency())