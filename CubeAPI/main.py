import json
import asyncio
import uvicorn
import socket
import threading
import time
import os

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

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

#  Basemodel used by calendar/add endpoint for calendar item structure
class Item(BaseModel):
    Title: str
    Description: str
    Location: str
    Date: str
    TimeStart: str

#  sets the day, time, and title as directories and filename. Then makes a JSON file in the specified folder
@app.post("/calendar/add")
def calendar_add(data: Item):
    day = data.Date
    hour = data.TimeStart
    title = data.Title

    # Checks if the directory exists, and makes one if it doesn't
    dirs = os.path.join("calendar", day, hour[0:2])
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    # checks if the file exists, and makes one if it doesn't
    path = os.path.join("calendar", day, hour[0:2], title + ".json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data.dict(), file, ensure_ascii=False, indent=4)
        return {
            "status": "SUCCES"
        }
    return {
        "status": "ALREADY EXISTS"
    }

@app.get("/calendar/days")
def list_days():
    path = os.path.join("calendar")
    list = []
    for obj in os.listdir(path):
        list.append(obj)
    if len(list) == 0:
        return "There are no items in your calendar"
    return list

@app.get("/calendar/items/{day}")
def list_items(day: str):
    path = os.path.join("calendar", day)
    if os.path.exists(path):
        list = []
        for obj in os.listdir(path):
            items = os.path.join("calendar", day, obj)
            for item in os.listdir(items):
                file = open(os.path.join("calendar", day, obj, item))
                data = json.loads(file.read())
                list.append(data["TimeStart"]+" - "+item[0:-5])
        return list
    return "There are no items planned that day"


# @app.get("/calendar/{calendar_options}")
# def calendar(calendar_options: SyncType) -> ReturnJSON:
#     if calendar_options is SyncType.SYNC:
#         pass
#     elif calendar_options is SyncType.GET:
#         return Calendar.getNext()
#     return ReturnJSON(detail=DetailJSON(message="", type=status.HTTP_200_OK))


@app.get("/timer/{ms}")
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


@app.get("/abort")
async def stop_timer():
    global is_timer_running
    is_timer_running = 0
    tts = TTS("je timer is gestopt")
    tts.play()
    return

