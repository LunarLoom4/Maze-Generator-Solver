import subprocess
import config
import os
import platform

def generate_video_from_frames(gen_algo, solve_algo):
    frame_dir = config.FRAME_DIR
    output_video = f"Maze_{config.GRID_HEIGHT}By{config.GRID_WIDTH}_Grid_{gen_algo.upper()}_{solve_algo.upper()}.mp4"
    framerate = 10

    if not os.path.exists(frame_dir):
        print(f"[FFMPEG] Frame directory does not exist: {frame_dir}")
        return

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(framerate),
        "-i", os.path.join(frame_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]

    print(f"[FFMPEG] Creating video: {output_video}...")
    subprocess.run(cmd)
    print(f"[FFMPEG] Done. Video saved as: {output_video}")

    # Removing the occurence of __pycache__ folder in each folder
    if platform.system() == "Windows":
        subprocess.run([
            "powershell",
            "-Command",
            "Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force"
        ])
    else:
        subprocess.run([
            "bash",
            "-c",
            "find . -type d -name '__pycache__' -exec rm -r {} +"
        ])
