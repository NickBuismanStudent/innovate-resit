import os
import platform
from gtts import gTTS
from src.log.log import Log


class TTS:
    def __init__(self, text: str, lang: str = "nl") -> None:
        self.text = text
        self.temp = "src\\tts\\temp.mp3"  # Still has to be fixed
        if platform.system() == "Windows":
            cmd = "start"
        else:
            cmd = "mpg321"
        self.cmd = f"{cmd} {self.temp}"
        self.gtts = gTTS(text=self.text, lang=lang, slow=False)
        self.gtts.save("src\\tts\\temp.mp3")  # Still has to be fixed
        Log(f"Created TTS -> {self.text}")

    def playboot(self) -> None:
        cmd = "mpg321"
        self.temp = "./CubeAPI/src/tts/setup.mp3"  # Still has to be fixed
        self.cmd = f"{cmd} {self.temp}"

    def play(self):
        os.system(self.cmd)
        Log(f"Played TTS -> {self.text}")

