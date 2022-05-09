import difflib
import random
import sys
import threading
import time
import speech_recognition as sr
from PyQt5 import QtWidgets, QtCore
from qtpy import QtGui
import win32api
import webbrowser
from interface import Ui_Window
from playsound import playsound

r = sr.Recognizer()


def get_difference(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def record_audio():
    microphone = sr.Microphone()
    with microphone as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=1)
    return audio


def recognize():
    response = {
        "success": True,
        "words": None
    }
    audio = record_audio()
    try:
        response["words"] = r.recognize_sphinx(audio)
    except:
        response["success"] = False
    return response


class mainWindow(QtWidgets.QMainWindow, Ui_Window):

    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_Window()
        self.ui.setupUi(self)
        self.status = 0
        self.lastStatus = 0
        self.commands = ["music", "notepad", "calculate", "browser"]

    def wakeUp(self):
        if self.status != 0:
            return
        if self.status == 0:
            self.gotoHello()
        response = recognize()
        if not response["success"]:
            self.startRecognize()
        else:
            if self.status != 0:
                return
            diff = get_difference(response["words"], "hello")
            if diff < 0.1:
                self.status = 0
                self.ui.NoListenLabel.setVisible(True)
                time.sleep(1)
                self.wakeUp()
            else:
                self.getHeard()

    def startRecognize(self):
        if self.status == 0:
            return
        elif self.status == 1 or self.status == 2:
            self.getHeard()

    def reStart(self):
        global timer
        timer.cancel()
        timer = threading.Timer(0.1, self.wakeUp)
        timer.setDaemon(True)
        timer.start()

    def getHeard(self):
        time.sleep(0.2)
        self.gotoListen()
        response = recognize()
        if self.status == 2:
            self.startRecognize()
        elif not response["success"]:
            self.startRecognize()
        else:
            command = response["words"]
            print('The statement you said is {' + command + '}')
            comps = [get_difference(command, element) for element in self.commands]
            max_similarity = max(comps)
            argmax_index = comps.index(max_similarity)
            if max_similarity < 0.2:
                self.ui.HelloLabel.setText("I guess you want to..")
                argmax_index = random.randint(0, 2)
            time.sleep(2)
            self.gotoRecognize()
            if argmax_index == 0:
                self.gotoMusic()
            elif argmax_index == 1:
                win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)
            elif argmax_index == 2:
                webbrowser.open("https://www.bing.com")
            else:
                win32api.ShellExecute(0, 'open', 'calc.exe', '', '', 1)

            time.sleep(2)
            self.status = 0
            self.reStart()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.status == 3 or self.status == 4:
            return
        if self.status == 2:
            if self.lastStatus == 0:
                self.gotoHello()
                self.reStart()
            elif self.lastStatus == 1:
                self.gotoListen()
        elif self.status == 0 or self.status == 1:
            self.gotoHelp()

    def gotoHello(self):
        self.lastStatus = self.status
        self.status = 0
        self.ui.WakeUpLabel.setVisible(False)
        self.ui.HelloLabel.setVisible(True)
        self.ui.BgLabel.setVisible(False)
        self.ui.BgLabel.setMovie(self.ui.bgStatic)
        self.ui.BgLabel.setVisible(True)
        self.ui.NoListenLabel.setVisible(False)
        self.ui.MusicLogoLabel.setVisible(False)
        self.ui.EnjoyMusicLabel.setVisible(False)
        self.ui.HintLabel.setVisible(False)
        self.ui.HelpTitleLabel.setVisible(False)
        self.ui.verticalLayoutWidget.setVisible(False)
        self.ui.HelpTitleLabel.setVisible(False)
        self.ui.HelpLabel.setGeometry(QtCore.QRect(75, 280, 151, 61))
        self.ui.HelpLabel.setText("Click to show command")
        self.ui.HelpLabel.setVisible(True)

    def gotoListen(self):
        self.lastStatus = self.status
        self.status = 1
        self.ui.verticalLayoutWidget.setVisible(False)
        self.ui.HelpTitleLabel.setVisible(False)
        self.ui.NoListenLabel.setVisible(False)
        self.ui.WakeUpLabel.setVisible(False)
        self.ui.HelloLabel.setVisible(False)
        self.ui.HelpLabel.setVisible(True)
        self.ui.WakeUpLabel.setVisible(True)
        self.ui.BgLabel.setMovie(self.ui.bgLive)
        self.ui.HelpLabel.setGeometry(QtCore.QRect(75, 280, 151, 61))
        self.ui.HelpLabel.setText("Click to show command")
        self.ui.HelpLabel.setVisible(True)

    def gotoHelp(self):
        self.lastStatus = self.status
        self.status = 2
        self.ui.BgLabel.setMovie(self.ui.bgClean)
        self.ui.HelpLabel.setGeometry(QtCore.QRect(75, 370, 151, 61))
        self.ui.HelpLabel.setText("Click to return")
        self.ui.verticalLayoutWidget.setVisible(True)
        self.ui.WakeUpLabel.setVisible(False)
        self.ui.HintLabel.setVisible(False)
        self.ui.NoListenLabel.setVisible(False)
        self.ui.HelpTitleLabel.setVisible(True)
        self.ui.HelloLabel.setVisible(False)

    def gotoRecognize(self):
        self.lastStatus = self.status
        self.status = 3
        self.ui.verticalLayoutWidget.setVisible(False)
        self.ui.HelpTitleLabel.setVisible(False)
        self.ui.HelpLabel.setVisible(False)
        self.ui.WakeUpLabel.setVisible(False)
        self.ui.HintLabel.setVisible(True)
        self.ui.NoListenLabel.setVisible(False)
        self.ui.BgLabel.setVisible(False)
        self.ui.BgLabel.setMovie(self.ui.bgLive)
        self.ui.BgLabel.setVisible(True)

    def gotoMusic(self):
        self.status = 4
        self.ui.HintLabel.setVisible(False)
        self.ui.BgLabel.setMovie(self.ui.bgClean)
        self.ui.MusicLogoLabel.setVisible(True)
        self.ui.EnjoyMusicLabel.setVisible(True)
        self.ui.NoListenLabel.setVisible(False)
        playsound('assets/名侦探.mp3')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    timer = threading.Timer(0.1, application.wakeUp)
    timer.setDaemon(True)
    timer.start()
    sys.exit(app.exec())
