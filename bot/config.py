import os
from dotenv import load_dotenv
load_dotenv('.env')

TOKEN = os.getenv('DISCORD_TOKEN')
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }