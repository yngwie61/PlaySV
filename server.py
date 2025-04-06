import os
import shutil
import threading
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer

MASTER_M3U8 = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="English",DEFAULT=YES,AUTOSELECT=YES,LANGUAGE="eng",URI="subtitles.m3u8"
#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720,SUBTITLES="subs"
playlist.m3u8
"""

SUBTITLES_M3U8 = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:16
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-PLAYLIST-TYPE:VOD

#EXTINF:60.0,
subtitles.vtt
#EXT-X-ENDLIST
"""

SUBTITLES_VTT = """WEBVTT

00:01.000 --> 00:05.000
Welcome to the Big Buck Bunny!

00:06.000 --> 00:10.000
This is a fun and engaging animated short film.

00:11.000 --> 00:15.000
Our story begins in a peaceful forest.

00:16.000 --> 00:20.000
Meet Big Buck Bunny, a friendly and curious character.

00:21.000 --> 00:25.000
He loves to explore and enjoy nature.

00:26.000 --> 00:30.000
One day, Bunny finds some unusual footprints.

00:31.000 --> 00:35.000
Curious, he decides to follow them.

00:36.000 --> 00:40.000
The trail leads him to a mysterious part of the forest.

00:41.000 --> 00:45.000
Here, Bunny discovers a hidden grove with strange creatures.

00:46.000 --> 00:50.000
The creatures are friendly but quite mischievous.

00:51.000 --> 00:55.000
Bunny and the creatures start to play and have fun.

00:56.000 --> 01:00.000
They engage in various games and activities.

01:01.000 --> 01:05.000
As the day goes on, Bunny and the creatures bond.

01:06.000 --> 01:10.000
The forest becomes a place of joy and laughter.

01:11.000 --> 01:15.000
Bunny learns the value of friendship and exploration.

01:16.000 --> 01:20.000
The adventure continues with many more exciting moments.

01:21.000 --> 01:25.000
Stay tuned for more fun and surprises!

01:26.000 --> 01:30.000
Big Buck Bunny's journey is filled with wonder.

01:31.000 --> 01:35.000
Enjoy the adventure and have a great time!

01:36.000 --> 01:40.000
The story is just beginning, and there's much more to come.

01:41.000 --> 01:45.000
Thank you for watching and being a part of this experience.

01:46.000 --> 01:50.000
We hope you enjoyed the film and had a lot of fun.

01:51.000 --> 01:55.000
Remember to always explore and find joy in new adventures.

01:56.000 --> 02:00.000
Until next time, keep smiling and enjoying life!

02:01.000 --> 02:05.000
The adventure continues in the magical world of Bunny.

02:06.000 --> 02:10.000
Stay curious and keep exploring!

02:11.000 --> 02:15.000
Bunny and friends will be back with more fun soon.

02:16.000 --> 02:20.000
Thank you for being part of this wonderful journey!

02:21.000 --> 02:25.000
We hope to see you again in future adventures.

02:26.000 --> 02:30.000
Enjoy the rest of the film and have a great day!

"""

FFMPEG_COMMAND = [
    "ffmpeg", "-re", "-i", "big_buck_bunny_1080p_h264.mov",
    "-map", "0:v", "-map", "0:a",
    "-s:v:0", "1280x720", "-c:v:0", "libx264", "-b:v:0", "3000k",
    "-maxrate:v:0", "3500k", "-bufsize:v:0", "6000k", "-g", "48",
    "-sc_threshold", "0", "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-ar", "44100",
    "-f", "hls", "-hls_time", "6", "-hls_playlist_type", "event",
    "-hls_segment_filename", "vv/segment_%03d.ts",
    "-var_stream_map", "v:0,a:0", "vv/playlist.m3u8"
]

def setup_vv_directory():
    # 1. Remove vv/ if exists
    if os.path.exists("vv"):
        shutil.rmtree("vv")
    os.makedirs("vv", exist_ok=True)

    # 2. Write master.m3u8
    with open("vv/master.m3u8", "w") as f:
        f.write(MASTER_M3U8)

    # 3. Write subtitles.m3u8
    with open("vv/subtitles.m3u8", "w") as f:
        f.write(SUBTITLES_M3U8)

    # 4. Write subtitles.vtt
    with open("vv/subtitles.vtt", "w") as f:
        f.write(SUBTITLES_VTT)

def run_ffmpeg():
    subprocess.run(FFMPEG_COMMAND)

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run(server_class=HTTPServer, handler_class=CORSHTTPRequestHandler, port=8000):
    setup_vv_directory()
    
    # ffmpeg実行を別スレッドで起動
    threading.Thread(target=run_ffmpeg, daemon=True).start()

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
