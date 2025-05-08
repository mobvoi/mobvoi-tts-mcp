import os, sys
import typing
import httpx
import json
import time
import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TextToSpeechClient:
    def __init__(self, *, app_key: str, app_secret: str, text2speech_client: typing.Union[httpx.Client, httpx.AsyncClient]):
        self._client = text2speech_client
        self._app_key = app_key
        self._app_secret = app_secret
        
    def text2speech_with_timestamps(
        self,
        *,
        text: str,
        speaker: typing.Optional[str] = None,
        audio_type: typing.Optional[str] = None,
        speed: typing.Optional[float] = 1.0,
        rate: typing.Optional[int] = 24000,
        volume: typing.Optional[float] = 1.0,
        pitch: typing.Optional[float] = 0,
        streaming: typing.Optional[bool] = False,
    ):
        timestamp = str(int(time.time()))
        message = '+'.join([self._app_key, self._app_secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        signature = m.hexdigest()
        
        request_data = {
            'text': text,
            'speaker': speaker,
            'audio_type': audio_type,
            'speed': speed,
            'rate': rate,
            'volume': volume,
            'pitch': pitch,
            'streaming': streaming,
            'gen_srt': False,
            'appkey': self._app_key,
            'timestamp': timestamp,
            'signature': signature,
        }
        print(f"request_data: {request_data}")
        try:
            _response = self._client.request(
                method="POST",
                url="https://open.mobvoi.com/api/tts/v1",    
            headers={
                "content-type": "application/json",
                },
                data=json.dumps(request_data)
            )
            print(f"response: {_response}")
            return _response.content
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
            return None

    async def async_text2speech_with_timestamps(
        self,
        *,
        text: str,
        speaker: typing.Optional[str] = None,
        audio_type: typing.Optional[str] = None,
        speed: typing.Optional[float] = 1.0,
        rate: typing.Optional[int] = 24000,
        volume: typing.Optional[float] = 1.0,
        pitch: typing.Optional[float] = 0,
        streaming: typing.Optional[bool] = False,
    ):
        if not isinstance(self._client, httpx.AsyncClient):
            raise ValueError("Client must be an instance of httpx.AsyncClient for async operations")
        timestamp = str(int(time.time()))
        message = '+'.join([self._app_key, self._app_secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        signature = m.hexdigest()
        
        request_data = {
            'text': text,
            'speaker': speaker,
            'audio_type': audio_type,
            'speed': speed,
            'rate': rate,
            'volume': volume,
            'pitch': pitch,
            'streaming': streaming,
            'gen_srt': False,
            'appkey': self._app_key,
            'timestamp': timestamp,
            'signature': signature,
        }
        logger.debug(f"request_data: {request_data}")
        # print(f"request_data: {request_data}")
        try:
            _response = await self._client.request(
                method="POST",
                url="https://open.mobvoi.com/api/tts/v1",    
                headers={
                    "content-type": "application/json",
                },
                data=json.dumps(request_data)
            )
            logger.debug(f"response: {_response}")
            # print(f"response: {_response}")
            return _response.content
        except Exception as e:
            logger.exception(f"Error: {e}")
            # print(f"Error: {e}")
            return None