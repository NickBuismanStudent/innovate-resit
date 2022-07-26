import json
import asyncio
import uvicorn
import socket
import threading
import time
from typing import Optional

from fastapi import FastAPI, status, Request

from src.calendar import Meeting, Calendar
from src.log.log import Log
from src.tts.TTS import TTS

app = FastAPI()
Log().cleanFile()

is_timer_running = 0
ip_set = 0

class BackgroundTasks(threading.Thread):
    def run(self):
        global ip_set
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        text = "mijn IP is "+ip
        while ip_set == 0:
            tts = TTS(text)
            tts.play()
            time.sleep(5)

# Currently disabled to prevent VLC from playing every 5 seconds
# @app.on_event("startup")
# async def startup_event():
#     t = BackgroundTasks()
#     t.start()

@app.get("/")
def main():
    return {"Message": "Hello"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

@app.get("/ip")
async def stop_echo():
    global ip_set
    ip_set = 1
    return

@app.get("/logs")
def getlog(date: Optional[str] = None):
    logs = Log()
    return logs.getLogs(date)

@app.get("/alert/{text}")
def alert(text: str):
    tts = TTS(text)
    tts.play()
    return {"detail": "Success"}

@app.post("/calendar/add")
async def calendar_add(data: Request):
    cal_info = await data.json()
    print(cal_info)
    return {
        "status" : "SUCCES",
        "data" : cal_info
    }

# @app.get("/calendar/{calendar_options}")
# def calendar(calendar_options: SyncType) -> ReturnJSON:
#     if calendar_options is SyncType.SYNC:
#         pass
#     elif calendar_options is SyncType.GET:
#         return Calendar.getNext()
#     return ReturnJSON(detail=DetailJSON(message="", type=status.HTTP_200_OK))

@app.post("/timer/{ms}")
async def timer(ms: int):
    global is_timer_running
    t = ms
    is_timer_running = 0
    is_timer_running = 1
    while t and is_timer_running:
        await asyncio.sleep(1)
        t -= 1000
    if is_timer_running:
        tts = TTS("je timer is voorbij")
        tts.play()
    is_timer_running = 0
    return

@app.post("/abort")
async def stop_timer():
    global is_timer_running
    is_timer_running = 0
    tts = TTS("je timer is gestopt")
    tts.play()
    return

