#! To extract individual frames from the mp4
mkdir _frames
ffmpeg -i "" _frames/frame_%06d.png
