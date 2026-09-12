import time

import os
import dotenv
from google import genai
import pyautogui
from io import BytesIO
import base64

import genie_tts as genie
from stt import record_once

genie.load_predefined_character('thirtyseven')

from PyQt6.QtCore import QTimerEvent, Qt
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication
from OpenGL.GL import *
from PyQt6.QtGui import QSurfaceFormat
import Resources

import live2d.v3 as live2d
# import live2d.v2 as live2d
os.environ["QSG_RHI_BACKEND"] = "opengl"


class Win(QOpenGLWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background:transparent")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.resize(400, 500)

        self.model: live2d.LAppModel | None = None

    def initializeGL(self) -> None:
        live2d.glInit()
        self.model = live2d.LAppModel()

        if live2d.LIVE2D_VERSION == 3:
            self.model.LoadModelJson(os.path.join("../Resources/v3/Haru/Haru.model3.json"))
        else:
            self.model.LoadModelJson(os.path.join("../Resources/v2/shizuku/shizuku.model.json"))

        self.startTimer(int(1000 / 120))

    def resizeGL(self, w: int, h: int) -> None:
        self.model.Resize(w, h)

    def paintGL(self) -> None:
        live2d.clearBuffer(0.7, 0.5, 0.4, 0)
        self.model.Update()

        self.model.Draw()

    def mouseMoveEvent(self, event):
        x, y = event.globalPosition().x() - self.x(), event.globalPosition().y() - self.y()
        self.model.Drag(x, y)
        speech = record_once()

        screenshot = pyautogui.screenshot()

        screenshot = screenshot.resize((768, 768))

        output = BytesIO()
        screenshot.save(output, format='PNG')
        im_data = output.getvalue()

        dotenv.load_dotenv()

        client = genai.Client(api_key=os.getenv("APIKEY"))

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=[
                {"type": "text", "text": "Keeping the response concise: " + speech},
                {
                    "type": "image",
                    "data": base64.b64encode(im_data).decode('utf-8'),
                    "mime_type": "image/png"
                },
            ],
        )

        output = interaction.output_text

        print(output)

        genie.tts(
            character_name='thirtyseven',
            text=output,
            play=True,
        )

        genie.wait_for_playback_done()

    def timerEvent(self, a0: QTimerEvent | None) -> None:
        self.update()

import sys

live2d.init()

app = QApplication(sys.argv)

win = Win()

win.show()
app.exec()

live2d.dispose()
