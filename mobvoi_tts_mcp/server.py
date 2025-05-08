import logging
import httpx
import typing
import os, sys
import mobvoi_tts_mcp
import asyncio
import time
from collections import deque

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# print(f"mobvoi_tts-mcp package location: {mobvoi_tts_mcp.__file__}")
logger.info(f"mobvoi-tts-mcp version: {mobvoi_tts_mcp.__version__}")
# logger.info("Running LOCAL version of mobvoi_tts_mcp server.py")

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from mobvoi_tts_sdk import MobvoiTTS
from mobvoi_tts_sdk import play
from mobvoi_tts_mcp.utils import (
    make_error,
    make_output_path,
    make_output_file,
    handle_input_file
)

load_dotenv()
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
base_path = os.getenv("MOBVOI_TTS_MCP_BASE_PATH")
print("base_path", base_path)
if not app_key:
    raise ValueError("Mobvoi_TTS_APP_KEY environment variable is required")
if not app_secret:
    raise ValueError("Mobvoi_TTS_app_secret environment variable is required")

custom_client = httpx.Client(
    timeout=10
)

async_custom_client = httpx.AsyncClient(
    timeout=10
)

# increase timeout for async client
# async_custom_client = httpx.AsyncClient(
#     timeout=httpx.Timeout(30.0, connect=60.0, read=30.0)
# )

# sync client instance
client = MobvoiTTS(
    app_key = app_key,
    app_secret = app_secret,
    httpx_client = custom_client
)

# async client instance
async_client = MobvoiTTS(
    app_key = app_key,
    app_secret = app_secret,
    httpx_client = async_custom_client
)

mcp = FastMCP("MobvoiTTS")

class RateLimiter:
    def __init__(self, rate_limit: int, time_window: float = 1.0):
        self.rate_limit = rate_limit  # Maximum number of requests per second
        self.time_window = time_window  # Time window (seconds)
        self.requests = deque()  # Store the request timestamp
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        async with self._lock:
            now = time.time()
            
            # Remove the request records outside the time window.
            while self.requests and now - self.requests[0] >= self.time_window:
                self.requests.popleft()
            
            # If the current number of requests reaches the limit, wait until the earliest request expires.
            if len(self.requests) >= self.rate_limit:
                wait_time = self.requests[0] + self.time_window - now
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                    return await self.acquire()
            
            # Add a new request timestamp
            self.requests.append(now)
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# Create a rate limiter instance to limit the requests to 5 per second. 
_RATE_LIMITER = RateLimiter(rate_limit=5)

@mcp.tool(
    description="""Async version of text_to_speech. Convert text to speech with a given speaker and save the output audio file to a given directory.
    Directory is optional, if not provided, the output file will be saved to $HOME/Desktop.
    You can choose speaker by providing speaker parameter. If speaker is not provided, the default speaker(xiaoyi_meet) will be used.
    
    ⚠️ COST WARNING: This tool makes an API call to Mobvoi TTS service which may incur costs. Only use when explicitly requested by the user.
    
    Args:
        text (str): The text to convert to speech.
        speaker (str): Determine which speaker's voice to be used to synthesize the audio.
        audio_type (str): Determine the format of the synthesized audio. Value can choose form [pcm/mp3/speex-wb-10/wav].
        speed (float): Control the speed of the synthesized audio. Values range from 0.5 to 2.0, with 1.0 being the default speed. Lower values create slower, more deliberate speech while higher values produce faster-paced speech. Extreme values can impact the quality of the generated speech. Range is 0.7 to 1.2.
        rate(int): Control the sampling rate of the synthesized audio. Value can choose from [8000/16000/24000], with 24000 being the deault rate.
        volume(float): Control the volume of the synthesized audio. Values range from 0.1 to 1.0,  with 1.0 being the default volume.
        pitch(float): Control the pitch of the synthesized audio. Values range from -10 to 10,  with 0 being the default pitch. If the parameter is less than 0, the pitch will become lower; otherwise, it will be higher.
        streaming(bool): Whether to output in a streaming manner. The default value is false.
        output_directory (str): Directory where files should be saved.
            Defaults to $HOME/Desktop if not provided.

    Returns:
        Text content with the path to the output file and name of the speaker used.
    """
)
async def async_text_to_speech(
    text: str,
    speaker: str = "xiaoyi_meet",
    audio_type: str = "mp3",
    speed: float = 1.0,
    rate: int = 24000,
    volume: float = 1.0,
    pitch: float = 0.0,
    streaming: bool = False,
    output_directory: typing.Optional[str] = None,
):
    logger.debug(f"async_text_to_speech start.")
    
    logger.debug(f"Received async_text_to_speech call: text={text}, speaker={speaker}, audio_type={audio_type}")
    
    if text == "":
        make_error("Text is required.")
    
    output_path = make_output_path(output_directory, base_path)
    output_file_name = make_output_file("tts", speaker, output_path, "mp3")
    
    logger.debug(f"Output path: {output_path / output_file_name}")
    
    async with _RATE_LIMITER:  # Use the rate limiter to control the request rate
        try:
            logger.debug("Calling Mobvoi TTS API")
            audio_data = await async_client.async_speech_generate(
                text=text,
                speaker=speaker,
                audio_type=audio_type,
                speed=speed,
                rate=rate,
                volume=volume,
                pitch=pitch,
                streaming=streaming
            )
            logger.debug(f"Received audio_data: {len(audio_data)} bytes")
            if len(audio_data) < 100:
                logger.error(f"Invalid audio data: {audio_data}")
                raise RuntimeError(f"Mobvoi TTS returned invalid data: {len(audio_data)} bytes")
            
        
            with open(output_path / output_file_name, "wb") as f:
                f.write(audio_data)
                logger.debug(f"Audio file written: {output_path / output_file_name}")
        
            return TextContent(
                type="text",
                text=f"Success. File saved as: {output_path / output_file_name}. Speaker used: {speaker}",
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"Mobvoi API error: {e.response.text}")
            raise RuntimeError(f"Mobvoi API failed: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Network error: {str(e)}")
            raise RuntimeError(f"Network error: {str(e)}")
        except Exception as e:
            logger.exception(f"Error in async_text_to_speech: {str(e)}")
            raise

@mcp.tool(
    description="""Async version of voice_clone. Clone a voice from a given url audio file. This tool will return a speaker id which can be used in text_to_speech tool.
    
    ⚠️ COST WARNING: This tool makes an API call to Mobvoi TTS service which may incur costs. Only use when explicitly requested by the user.
    
    Args:
        wav_uri (str): The url of the audio file to clone.
    """
)
async def async_voice_clone_url(wav_uri: str):
    logger.debug(f"Received wav_uri from {wav_uri}")
    async with _RATE_LIMITER:
        try:
            speaker = await async_client.async_voice_clone_url(wav_uri=wav_uri)
            return TextContent(
                type="text",
                text=f"Success. Speaker id: {speaker}",
            )
        except Exception as e:
            logger.exception(f"Error in async_voice_clone_url: {str(e)}")
            raise

@mcp.tool(
    description="""Async version of voice_clone. Clone a voice from a given local audio file. This tool will return a speaker id which can be used in text_to_speech tool.
    
    ⚠️ COST WARNING: This tool makes an API call to Mobvoi TTS service which may incur costs. Only use when explicitly requested by the user.
    
    Args:
        audio_file_path (str): The path of the audio file to clone.
    """
)
async def async_voice_clone_local(audio_file_path: str):
    logger.debug(f"Received audio_file_path from {audio_file_path}")
    async with _RATE_LIMITER:
        try:
            speaker = await async_client.async_voice_clone_local(audio_file_path=audio_file_path)
            return TextContent(
                type="text",
                text=f"Success. Speaker id: {speaker}",
            )   
        except Exception as e:
            logger.exception(f"Error in async_voice_clone_local: {str(e)}")
            raise

@mcp.tool(description="Play an audio file. Supports WAV and MP3 formats.")
def play_audio(input_file_path: str) -> TextContent:
    file_path = handle_input_file(input_file_path)
    play(open(file_path, "rb").read(), use_ffmpeg=False)
    return TextContent(type="text", text=f"Successfully played audio file: {file_path}")

def main():
    logger.info("Starting MCP server")
    mcp.run()


if __name__ == "__main__":
    main()