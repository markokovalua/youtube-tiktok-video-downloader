from fastapi import (
    FastAPI,
    HTTPException,
    BackgroundTasks,
    WebSocketDisconnect,
    WebSocket,
)
from pydantic import BaseModel
from fastapi.responses import FileResponse
import yt_dlp
import logging
import asyncio
import os
from uuid import uuid4

app = FastAPI()


class VideoURL(BaseModel):
    url: str


logger = logging.getLogger(__name__)

progress_queues = {}

def sync_download(url: str, download_id: str):
    ydl_opts = {
        "outtmpl": "/downloads/%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "concurrent_fragment_downloads": 10,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)  # Just get metadata
            filename = ydl.prepare_filename(info)
            ydl.download([url])
            return filename
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error deleting file: {str(e)}"
            )


@app.post("/download/")
async def download_video(video_url: VideoURL):
    try:
        download_id = str(uuid4())
        filepath = await asyncio.to_thread(sync_download, video_url.url, download_id)
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="video/mp4",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))