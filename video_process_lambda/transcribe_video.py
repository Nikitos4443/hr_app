from config import model


# faster-whisper decodes the video itself via PyAV, so no separate ffmpeg step is needed
def transcribe(path_to_video: str) -> str:
    segments, _ = model.transcribe(path_to_video, language="en")
    return "".join(segment.text for segment in segments)
