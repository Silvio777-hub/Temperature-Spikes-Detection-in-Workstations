import argparse
import platform
import subprocess
import sys
from pathlib import Path

def check_ffmpeg() -> bool:
    """Check if ffmpeg is available in PATH.
    Returns True if ffmpeg can be executed, False otherwise.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def build_ffmpeg_cmd(output: Path, duration: int, fps: int = 30, region: str = None) -> list:
    """Construct ffmpeg command for screen recording.
    Args:
        output: Path to output video file.
        duration: Recording duration in seconds.
        fps: Frames per second.
        region: Optional region string for Windows ("left,top,width,height").
    Returns:
        List of command arguments.
    """
    system = platform.system().lower()
    if system == "windows":
        # Use gdigrab on Windows
        input_source = "desktop"
        cmd = ["ffmpeg", "-f", "gdigrab", "-framerate", str(fps), "-i", input_source]
        if region:
            # region format: left,top,width,height
            left, top, width, height = region.split(",")
            cmd.extend(["-vf", f"crop={width}:{height}:{left}:{top}"])
    elif system == "linux":
        # Use x11grab on Linux
        display = ":0.0"
        input_source = f"{display}"
        cmd = ["ffmpeg", "-f", "x11grab", "-framerate", str(fps), "-i", input_source]
        if region:
            left, top, width, height = region.split(",")
            cmd.extend(["-vf", f"crop={width}:{height}:{left}:{top}"])
    elif system == "darwin":
        # macOS uses avfoundation
        input_source = "1:none"
        cmd = ["ffmpeg", "-f", "avfoundation", "-framerate", str(fps), "-i", input_source]
        # macOS cropping can be added with -vf if needed
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    cmd.extend([
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        str(output)
    ])
    return cmd

def main():
    parser = argparse.ArgumentParser(description="Simple screen recorder using ffmpeg.")
    parser.add_argument("--duration", type=int, default=60, help="Recording length in seconds (default: 60)")
    parser.add_argument("--output", type=str, default="recording.mp4", help="Output video filename")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    parser.add_argument("--region", type=str, help="Optional crop region as left,top,width,height")
    args = parser.parse_args()

    if not check_ffmpeg():
        sys.exit("ffmpeg not found in PATH. Please install ffmpeg and add it to your system PATH.")

    output_path = Path(args.output).expanduser().resolve()
    cmd = build_ffmpeg_cmd(output_path, args.duration, args.fps, args.region)
    print(f"Starting recording: {output_path} (duration: {args.duration}s)")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"ffmpeg failed with error: {e}")
    print("Recording completed.")

if __name__ == "__main__":
    main()
