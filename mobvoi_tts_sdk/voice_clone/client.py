import os, sys
import typing
import httpx
import json
import time
import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VoiceCloneClient:
    def __init__(self, *, app_key: str, app_secret: str, voice_clone_client: typing.Union[httpx.Client, httpx.AsyncClient]):
        self._client = voice_clone_client
        self._app_key = app_key
        self._app_secret = app_secret
        
    def clone_url(self, *, wav_uri: str):
        logger.debug(f"wav_uri: {wav_uri}")
        timestamp = str(int(time.time()))
        message = '+'.join([self._app_key, self._app_secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        signature = m.hexdigest()
        request_data = {
            'appKey': self._app_key,
            'signature': signature,
            'timestamp': timestamp,
            'wavUri': wav_uri,
        }
        try:
            _response = self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data
            )
            if _response.json()['code'] == 0:
                logger.debug("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            print(f"Error: {e}")
    
    async def async_clone_url(self, *, wav_uri: str):
        logger.debug(f"wav_uri: {wav_uri}")
        timestamp = str(int(time.time()))
        message = '+'.join([self._app_key, self._app_secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        signature = m.hexdigest()
        
        request_data = {
            'appKey': self._app_key,
            'signature': signature,
            'timestamp': timestamp,
            'wavUri': wav_uri,
        }
        try:
            _response = await self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data
            )
            if _response.json()['code'] == 0:
                print("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
    
    def clone_local(self, *, audio_file_path: str):
        logger.debug(f"audio_file_path: {audio_file_path}")
        timestamp = str(int(time.time()))
        message = '+'.join([self._app_key, self._app_secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        signature = m.hexdigest()
        request_data = {
            'appKey': self._app_key,
            'signature': signature,
            'timestamp': timestamp,
        }
        files = {
            'file': open(audio_file_path, 'rb')
        }
        try:
            _response = self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data,
                files=files
            )
            if _response.json()['code'] == 0:
                print("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
            return None
            
    async def async_clone_local(self, *, audio_file_path: str):
        logger.debug(f"audio_file_path: {audio_file_path}")
        timestamp = str(int(time.time()))
        message = '+'.join([self._app_key, self._app_secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        signature = m.hexdigest()
        request_data = {
            'appKey': self._app_key,
            'signature': signature,
            'timestamp': timestamp,
        }
        files = {
            'file': open(audio_file_path, 'rb')
        }
        try:
            _response = await self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data,
                files=files
            )
            if _response.json()['code'] == 0:
                logger.debug("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
            return None