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

def remove_stop_words(poem):
    stop_words = open(r'db\stop_words.txt', 'r', encoding='utf-8').readlines()
    stop_words = [i.strip() for i in stop_words]

    poem = poem.split(' ')

    normal_words = []

    for i in range(len(poem)):
        if poem[i] not in stop_words:
            normal_words.append(poem[i])

    unique_normal_words = []
    for i in normal_words:
        if i not in unique_normal_words:
            unique_normal_words.append(i)

    return unique_normal_words

def contain_valid_word(first_words, second_words):
    if type(first_words) != list:
        first_words = remove_stop_words(first_words)
    if type(second_words) != list:
        second_words = remove_stop_words(second_words)

    for i in first_words:
        if i in second_words:
            return True
            break
    else:
        return False

def start(self, app, stt, speaker):
    poems = open(r'db\poems\main_poems.csv', 'r', encoding='utf-8').readlines()
    poems = [i.strip().replace(',', ' / ') for i in poems]

    sound_poems = open(r'db\poems\sound_poems.csv', 'r', encoding='utf-8').readlines()
    sound_poems = [i.strip().split(',') for i in sound_poems]

    black_list = []
    current_last_words = []
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

                user_normal_words = remove_stop_words(user_poem)

                if current_last_words != [] and contain_valid_word(user_normal_words, current_last_words):
                    break
                elif current_last_words == []:
                    break
        else:
            if current_last_words != [] and not contain_valid_word(user_normal_words, current_last_words):
                self.notice.setText('شعر شما باید حاوی حداقل یک کلمه از شعر قبل باشد')
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
            if contain_valid_word(f'{i[1]} {i[2]}', user_normal_words):
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

        current_last_words = remove_stop_words(f'{machine_poem[1]} {machine_poem[2]}')

        black_list.append(f"{machine_poem[1]} {machine_poem[2]}")
        black_list.append(f"{machine_poem[3]} {machine_poem[4]}")

        score += 1
        update_record(score, 1)
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
        self.speak.setText(','.join(current_last_words))
        app.processEvents()