# Global libs
import speech_recognition as sr
from playsound import playsound
from PyQt5.QtGui import QIcon
import random
import os

# Local libs
from scripts.records import update_record
from scripts.normalize import normalize
from scripts.similar import similar
from scripts import record_poem


def start(self, app, stt, speaker):
    poems = open(r'db\poems\main_poems.csv', 'r', encoding='utf-8').readlines()
    poems = [i.strip().replace(',', ' / ') for i in poems]

    sound_poems = open(r'db\poems\sound_poems.csv', 'r', encoding='utf-8').readlines()
    sound_poems = [i.strip().split(',') for i in sound_poems]

    black_list = []
    current_last_char = ''
    score = 0

    while 1:
        try:
            if stt == 'online':
                user_poem = record_poem.online()
            else:
                user_poem = record_poem.offline()
        except TypeError:
            self.notice.setText('ضبط صدا با خطا مواجه شد، لطفا دوباره امتحان کنید')
            app.processEvents()
            continue
        except sr.WaitTimeoutError:
            self.notice.setText('ضبط صدا با خطا مواجه شد، لطفا دوباره امتحان کنید')
            app.processEvents()
            continue

        user_poem = normalize(user_poem)

        for i in poems:
            if similar(user_poem.replace(' / ', ' '), i) > 0.5:
                user_poem = i

                self.poem_box.setText(user_poem)
                app.processEvents()

                user_poem = user_poem.replace(' / ', ' ')

                user_first_char = user_poem[0]
                user_last_char = user_poem[-1]

                if current_last_char != '' and user_first_char == current_last_char:
                    break
                elif current_last_char == '':
                    break
        else:
            if current_last_char != '' and user_first_char != current_last_char:
                self.notice.setText('شعر شما باید با آخرین حرف شعر قبلی شروع شود')
                app.processEvents()
            else:
                self.notice.setText("شعر شما اشتباه است یا در دیتابیس وجود ندارد")
                app.processEvents()
            continue

        if user_poem in black_list:
            self.notice.setText('شعر شما تکراری است!')
            app.processEvents()
            continue

        black_list.append(user_poem)

        candidates = []

        for i in sound_poems:
            if i[1][0] in user_last_char:
                if f"{i[1]} {i[2]}" not in black_list:
                    candidates.append(i)

        if speaker == 'first_speaker':
            candidates = [i for i in candidates if int(i[0]) < 179]
        elif speaker == 'second_speaker':
            candidates = [i for i in candidates if int(i[0]) > 178]

        try:
            machine_poem = random.choice(candidates)
        except IndexError:
            self.notice.setText('من تسلیم می شوم ! تبریک، شما برنده شدید')
            self.speak.setText('برنده شدید')
            self.poem_box.clear()
            break
        
        current_last_char = machine_poem[-1][-1]

        black_list.append(f"{machine_poem[1]} {machine_poem[2]}")
        black_list.append(f"{machine_poem[3]} {machine_poem[4]}")

        score += 1
        update_record(score, 2)
        self.score.setText(f"امتیاز: {str(score)}")

        self.notice.setText("گوش دهید")
        self.speak.setText('. . .')
        app.processEvents()

        try:
            playsound(f"db\\sounds\\{machine_poem[0]}.mp3")
        except:
            pass

        self.notice.setText("شعر خود را بگویید")
        self.speak.setIcon(QIcon())
        self.speak.setText(current_last_char)
        app.processEvents()