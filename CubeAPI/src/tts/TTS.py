import os
import platform
from gtts import gTTS
from src.log.log import Log


class TTS:
    def __init__(self, text: str, lang: str = "en") -> None:
        self.text = text
        if platform.system() == "Windows":
            self.temp = "src\\tts\\temp.mp3"
            cmd = "start"
            save = "src\\tts\\temp.mp3"
        else:
            self.temp = "./CubeAPI/src/tts/temp.mp3"
            cmd = "mpg321"
            save = "./CubeAPI/src/tts/temp.mp3"
        self.cmd = f"{cmd} {self.temp}"
        self.gtts = gTTS(text=self.text, lang=lang, slow=False)
        self.gtts.save(save)
        Log(f"Created TTS -> {self.text}")

    def play(self):
        os.system(self.cmd)
        Log(f"Played TTS -> {self.text}")

