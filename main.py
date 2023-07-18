# Global libs
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QThread
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import subprocess
import webbrowser
import shutil
import sys
import os

# Local libs
from scripts.settings import update_settings
from scripts.settings import read_settings
from scripts.records import get_record
from scripts import traditional
from scripts import words
from scripts import hard


if not os.path.exists(rf'C:\Users\{os.getlogin()}\.cache\vosk\vosk-model-small-fa-0.5'):
    if not os.path.exists(rf"C:\Users\{os.getlogin()}\.cache"):
        os.mkdir(rf"C:\Users\{os.getlogin()}\.cache")
    if not os.path.exists(rf"C:\Users\{os.getlogin()}\.cache\vosk"):
        os.mkdir(rf"C:\Users\{os.getlogin()}\.cache\vosk")
    
    shutil.copytree("vosk-model-small-fa-0.5", rf"C:\Users\{os.getlogin()}\.cache\vosk\vosk-model-small-fa-0.5")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.showMaximized()

        self.traditional.clicked.connect(self.load_traditional_game)
        self.words.clicked.connect(self.load_words_game)
        self.hard.clicked.connect(self.load_hard_game)
        self.bank.clicked.connect(self.load_poem_bank)
        self.practice.clicked.connect(self.load_practice)
        self.settings.clicked.connect(self.load_settings)
        self.contribute.clicked.connect(self.open_github_page)
        self.guid.clicked.connect(self.show_guid)

    
    def show_guid(self):
        self.guid = guid()
        guid.show_guid(self.guid, "main")
        self.guid.show()

    def load_traditional_game(self):
        global game_pages
        game_pages = game_pages(game_mode='traditional')
        game_pages.show()
        game_pages.setGeometry(self.geometry())
        self.close()
    
    def load_words_game(self):
        global game_pages
        game_pages = game_pages(game_mode='words')
        game_pages.show()
        game_pages.setGeometry(self.geometry())
        self.close()

    def load_hard_game(self):
        global game_pages
        game_pages = game_pages(game_mode='hard')
        game_pages.show()
        game_pages.setGeometry(self.geometry())
        self.close()

    def load_poem_bank(self):
        global poem_bank
        poem_bank = poem_bank()
        poem_bank.show()
        poem_bank.setGeometry(self.geometry())
        self.close()

    def load_practice(self):
        global message_box

        try:
            message_box = message_box(message="! این بخش بزودی به برنامه اضافه می شود")
        except TypeError:
            pass

        message_box.show()
        # set the message_box in the center of the MainWindow
        message_box.move(int(self.size().width()/2) - int(message_box.size().width()/2) + self.pos().x(), 
                         int(self.size().height()/2) - int(message_box.size().height()/2) + self.pos().y())

    def load_settings(self):
        global settings
        settings = settings()
        settings.show()
        settings.setGeometry(self.geometry())
        self.close()

    def open_github_page(self):
        webbrowser.open("https://github.com/ali-hv")


class guid(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/guid.ui', self)

        app.setStyleSheet(stylesheet)

    def show_guid(self, page):
        guids = {'main': 'راهنما', 'traditional': 'مشاعره سنتی', 'words': 'مشاعره کلمه ای', 'hard': 'مشاعره سخت', 'poem_bank': 'گنجینه', 'settings': 'تنظیمات'}

        self.title.setText(guids[page])
        self.guid_text.setHtml(open(f"guids/{page}_guid.txt", "r", encoding="utf-8").read())


class start_game(QObject):
    finished = pyqtSignal()
    def __init__(self, game_self, app, game_mode, parent=None):
        QThread.__init__(self, parent)
        self.game_self, self.app, self.game_mode = game_self, app, game_mode

    def run(self):
        if self.game_mode == 'traditional':
            traditional.start(self.game_self, self.app, stt, speaker)
        elif self.game_mode == 'words':
            words.start(self.game_self, self.app, stt, speaker)
        elif self.game_mode == 'hard':
            hard.start(self.game_self, self.app, stt, speaker)

class game_pages(QWidget):
    def __init__(self, game_mode):
        super().__init__()
        self.game_mode = game_mode
        uic.loadUi('ui/game.ui', self)
        
        app.setStyleSheet(stylesheet)

        if self.game_mode == 'traditional':
            self.title.setText('مشاعره سنتی')
            self.record.setText(f"رکورد: {get_record(0)}")
        elif self.game_mode == 'words':
            self.title.setText('مشاعره کلمه ای')
            self.record.setText(f"رکورد: {get_record(1)}")
        elif self.game_mode == 'hard':
            self.title.setText('مشاعره سخت')
            self.record.setText(f"رکورد: {get_record(2)}")

        self.back.clicked.connect(self.back_menu)
        self.guid.clicked.connect(self.show_guid)
        self.play.clicked.connect(self.play_button)
        self.speak.clicked.connect(self.start_game)

    def show_guid(self):
        self.guid = guid()
        guid.show_guid(self.guid, self.game_mode)
        self.guid.show()

    def back_menu(self):
        subprocess.Popen(['python', 'main.py'])
        self.close()

    def play_button(self):
        self.play.hide()
        self.notice.show()
        self.poem_box.show()
        self.speak.show()
        self.notice.setText("روی دکمه ضبط صدا کلیک کنید و شعر خود را بگویید")

    def start_game(self):
        self.speak.setDisabled(True)
        self.speak.setStyleSheet("icon: url();")
        self.speak.setText('. . .')

        self.thread = QThread(parent=self)
        self.worker = start_game(game_self=self, app=app, game_mode=self.game_mode)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.notice.setText('شعر خود را بگویید')


class poem_bank(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/poem_bank.ui', self)

        app.setStyleSheet(stylesheet)

        self.back.clicked.connect(self.back_menu)
        self.guid.clicked.connect(self.show_guid)
        self.poet_search_bar.textChanged.connect(self.search_poet)
        self.poem_search_bar.textChanged.connect(self.search_poem)

        self.poems = open('db/poems/all_poems.txt', 'r', encoding="utf-8").readlines()
        self.poems = [i.strip() for i in self.poems]

        self.poets_name = open('db/poets_name.txt', 'r', encoding="utf-8").readlines()
        self.poets_name = [i.strip() for i in self.poets_name]

        for i in self.poets_name:
            eval(f"self.{i}.clicked.connect(lambda: poem_bank.show_poems('{i}'))")

    def back_menu(self):
        subprocess.Popen(['python', 'main.py'])
        self.close()

    def show_guid(self):
        self.guid = guid()
        guid.show_guid(self.guid, 'poem_bank')
        self.guid.show()

    def show_poems(self, poet_name):
        self.poem_box.clear()
        self.poem_search_bar.clear()
        poems = open(f'db/persian poems/{poet_name}_norm.txt', 'r', encoding="utf-8").readlines()

        poems_html = '<html><head/><body>'

        for i in poems:
            poems_html += f'<p align="center">{i}</p>'
            #self.poem_box.append(f'<p align="center">{i}</p></body></html>')

        poems_html += '</body></html>'
        self.poem_box.setHtml(poems_html)

        self.poem_box.verticalScrollBar().setValue(0)

    def search_poet(self):
        for i in self.poets_name:
            eval(f"self.{i}.hide()")

        for i in self.poets_name:
            if self.poet_search_bar.text() in eval(f"self.{i}.text()"):
                eval(f"self.{i}.show()")

    def search_poem(self):
        self.poem_box.clear()
        text = self.poem_search_bar.text()
        if len(text) > 4:
            res = []
            for i in self.poems:
                if text in i:
                    res.append(i)

            for i in res:
                self.poem_box.append(f'<html><head/><body><p align="center">{i}</p></body></html>')

        self.poem_box.verticalScrollBar().setValue(0)

class message_box(QWidget):
    def __init__(self, message):
        super().__init__()
        self.message = message
        uic.loadUi('ui/message_box.ui', self)


class settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/settings.ui', self)

        app.setStyleSheet(stylesheet)

        self.back.clicked.connect(self.back_menu)
        self.guid.clicked.connect(self.show_guid)

        settings_radio_btns = {'blue':'theme', 'white':'theme', 'first_speaker':'speaker', 'second_speaker':'speaker',
                              'combine':'speaker', 'online':'stt', 'offline':'stt'}
        for i in settings_radio_btns:
            eval(f"self.{i}.clicked.connect(lambda: update_settings('{settings_radio_btns[i]}', '{i}'))")
        
        if theme == 'blue':
            self.blue.setChecked(True)
        elif theme == 'white':
            self.white.setChecked(True)
        if speaker == 'combine':
            self.combine.setChecked(True)
        elif speaker == 'first_speaker':
            self.first_speaker.setChecked(True)
        elif speaker == 'second_speaker':
            self.second_speaker.setChecked(True)
        if stt == 'online':
            self.online.setChecked(True)
        elif stt == 'offline':
            self.offline.setChecked(True)

    def back_menu(self):
        subprocess.Popen(['python', 'main.py'])
        self.close()

    def show_guid(self):
        self.guid = guid()
        guid.show_guid(self.guid, 'settings')
        self.guid.show()

if __name__ == "__main__":
    theme, speaker, stt = read_settings()
    stylesheet = open(fr"qss\{theme}.qss", "r").read()
    app = QApplication(sys.argv)
    app.setStyle("windows")
    app.setStyleSheet(stylesheet)
    QtGui.QFontDatabase.addApplicationFont("fonts/Lalezar.ttf")
    Lalezar_font = QtGui.QFont()
    Lalezar_font.setFamily("Lalezar")
    app.setFont(Lalezar_font) 
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())