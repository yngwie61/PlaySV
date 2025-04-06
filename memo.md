## 起動方法

python server.pyを実行

実行時の内部処理は以下の手順で実行

1. vv/以下のディレクトリのファイルを全て削除
2. master.m3u8を出力(playlist.m3u8とsubtitles.m3u8を参照)
3. subtitles.m3u8(.vtt)を出力
4. ffmpegのコマンドを実行(playlist.m3u8をカレントディレクトリの.movファイルに対して出力する)
5. HTTPサーバ起動

## 以下のコマンドを実行

ffmpeg -re -i big_buck_bunny_1080p_h264.mov \
  -map 0:v -map 0:a \
  -s:v:0 1280x720 -c:v:0 libx264 -b:v:0 3000k -maxrate:v:0 3500k -bufsize:v:0 6000k -g 48 -sc_threshold 0 \
  -c:a aac -b:a 128k -ac 2 -ar 44100 \
  -f hls -hls_time 6 -hls_playlist_type event \
  -hls_segment_filename "vv/segment_%03d.ts" \
  -var_stream_map "v:0,a:0" \
  vv/playlist.m3u8
