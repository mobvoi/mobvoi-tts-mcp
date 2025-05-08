from mobvoi_tts_mcp.utils import handle_input_file
from mobvoi_tts_sdk import play

input_file_path = "/Users/kk/Desktop/tts_galaxy_f_20250507_094710.mp3"
file_path = handle_input_file(input_file_path)
play(open(file_path, "rb").read(), use_ffmpeg=False)