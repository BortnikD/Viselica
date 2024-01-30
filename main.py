import tkinter  # для работы с визуализацией
import time   # для плавной отрисовки различных фрагментов интерфейса, со временем будет удалена
import json  # для преобразования данных из words.json
import random  # ну какая игры без элементов случайности?)


class Grafik(tkinter.Canvas):  # класс для основной отрисовки игры
    def __init__(self, window):
        super().__init__(window, width=1080, height=1080, bg='skyblue')
        self.heart_image = tkinter.PhotoImage(file='hearts.png')  # картинка сердца, используется в create_health_scale
        self.hearts = []
        #self.human = []

    def create_map(self):  # метод для создания карты, земля, солнце, виселица
        earth = self.create_rectangle(0, 880, 1080, 1080, fill='green')
        sun = self.create_oval(-80, -80, 150, 150, fill='yellow')

        pillar = self.create_rectangle(800, 200, 820, 880, fill='brown')
        branch = self.create_rectangle(600, 200, 800, 220, fill='brown')
        rope = self.create_line(610, 220, 610, 320)
        a_loop = self.create_oval(590, 320, 630, 360)

    def create_human(self):  # метод для создания человека
        leg_1 = self.create_line(200, 880, 220, 800, width=5)
        leg_2 = self.create_line(220, 800, 240, 880, width=5)
        torse = self.create_line(220, 710, 220, 800, width=5)
        head = self.create_oval(200, 710, 240, 670, fill='black')
        hand_1 = self.create_line(200, 800, 220, 715, width=5)
        hand_2 = self.create_line(220, 715, 240, 800, width=5)

        self.human = [leg_1, leg_2, torse, head, hand_1, hand_2]

    def human_move(self, dx, dy=0):  # функция для передвижения человека
        for part in self.human:
            self.move(part, dx, dy)

    def create_health_scale(self, attempts):  # функция для отрисовки жизней
        image_path = 'hearts.png'
        move_heath = 0
        for _ in range(attempts):
            move_heath += 35
            heart = self.create_image(1000 - move_heath, 50, image=self.heart_image)
            self.hearts.append(heart)
            time.sleep(0.2)
            self.update()

    def update_health_scale(self, attempts):  # удаление сердечка в случае неудачной попытки
        # отнимаем от начального количества попыток те, что остались, а также -1, для того чтобы
        # сердце под номером 0 тоже удалилось
        ind = 7 - attempts - 1
        if ind >= 0:
            heart_id = self.hearts[ind]  # Получаем идентификатор сердечка из списка
            self.delete(heart_id)  # Удаляем сердечко с холста

    def delete_all(self):  # очищение всего холста, остается только окно
        self.delete('all')
        for lbl in tk_window.winfo_children():
            lbl.destroy()

    def create_loss_wind(self):  # обновленное окно в случае проигрыша
        for lbl in label_list:
            lbl.destroy()
        game_entry.destroy()
        self.human_move(390, -350)
        self.create_text(250, 450, font=('Arial', 30), text=f'Вы проиграли =(\nЗагаданное слово - {word_glob}')

    def create_win_wind(self):  # создание окна в случае победы
        self.delete_all()
        canvas = tkinter.Canvas(tk_window, width=900, height=900, bg='yellow')
        canvas.pack()
        canvas.create_text(450, 450, font=('Arial', 30), text='Вы выиграли! =D')


class InputsDates(tkinter.Entry):  # класс для обработки входных данных
    def __init__(self, window, letter=None):
        super().__init__(window, width=2, font=('Arial', 30), bg='lightgreen')
        self.letter = letter

    def dates_get(self, event):  # получение данных из ввода в виджет
        self.letter = game_entry.get()[:1]  # берем только первый символ
        game_entry.delete(0, tkinter.END)  # очищаем виджет после ввода
        rules.input_letter(self.letter)  # проверяем есть ли эти данные в слове


class Rules():  # класс с правилами игры
    def __init__(self, window, word=None):
        self.word = word

    def choice_word(self):  # выбор слова из файла со словами
        with open('words.json') as file:
            words = file.read()
            words_js = json.loads(words)
            self.word = random.choice(words_js)
            return self.word

    def input_letter(self, letter):  # Проверка наличия буквы в слове, вызывается в методе dates_get()
        print(letter, '-', self.word, 'в', self.word.find(letter))
        if letter.lower() in self.word.lower():
            for i in range(len(self.word)):
                if self.word[i].lower() == letter.lower():
                    label_list[i].config(text=letter)
            self.check_win()
        else:
            self.check_loss()

    def check_win(self):  # проверка на победу
        label_txt = ''
        for lbl in label_list:
            label_txt += lbl['text']
        if label_txt.lower() == self.word.lower():
            game.create_win_wind()

    def check_loss(self):  # проверка на поражение
        global atts
        atts -= 1
        if atts != 0:
            game.update_health_scale(atts)
        else:
            game.update_health_scale(atts)
            game.create_loss_wind()


# создание окна и холста
tk_window = tkinter.Tk()
game = Grafik(tk_window)
game.pack()

# создаем визуальную часть игры, карту, человека, шкалу здоровья
game.create_map()
game.create_human()
atts = 7
game.create_health_scale(atts)

# создание виджета для ввода букв и размешение его в нужной точке
game_entry = InputsDates(tk_window)
game_entry.pack()
game_entry.place(x=50, y=300)

# выбираем слово, начинаем проверку игры
rules = Rules(tk_window)
word_glob = rules.choice_word()

# создание виджетов для отображения букв, угаданных и нет
label_list = []
for i, letter in enumerate(word_glob):
    move_lab = i * 40
    label = tkinter.Label(tk_window, text='', width=2, font=('Arial', 20), bg='cornsilk')
    label.place(x=50 + move_lab, y=400)
    label_list.append(label)
    tk_window.update()
    time.sleep(0.2)

# привязываем нажатие enter к вызову функции для получения введеных данных в виджет
game_entry.bind('<Return>', game_entry.dates_get)

tk_window.mainloop()  # удерживаем окно открытым
