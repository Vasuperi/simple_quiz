from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image 
from kivy.core.window import Window 
from kivy.clock import Clock
from ctypes import windll
from os import name as sysname
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle, Ellipse
from random import choice

#TODO сделать расширение под андроид систему (определение ширины окна,
#  вместо пол экрана занять весь по высоте, запретить перевернуть экран в вертик,
#  подогнать размер шрифта)
if sysname == 'nt':
    su = windll.user32
    screensize = su.GetSystemMetrics(0), su.GetSystemMetrics(1)
else:
    screensize = (800,600)

class QuizApp(App):
    
    soundfile = None
    button_porp = "create"
    def_instance = None
    after_press_right = None
    timer_event = None  # объект события таймера
    sound = None       

    def on_start(self):             
        # Рассчитываем новый размер окна
        new_window_width = int(screensize[0] * 2 / 3)
        new_window_height = int(screensize[1] *0.25)
        
        # Меняем размер окна
        Window.size = (new_window_width, new_window_height)    

    def build(self):
        root = FloatLayout() 
        # Основной вертикальный слой 
        self.main_layout = FloatLayout(size_hint=(1, 1))
        with self.main_layout.canvas.before:
            Color(.12, .43, .72, 1)  # Установили голубой фон для общего Layout
            self.background_rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        
        self.main_layout.bind(pos=self.update_rectangle_main, size=self.update_rectangle_main)

        # Верхняя треть экрана — текстовый элемент
        self.text_widget = Label(
            text="[b]Привет, мир![/b]",markup = True,
            size_hint=(1, 1 / 3),
            pos_hint={"top": 1 , 'left':0.8}                     
        )
                                          
        # Нижняя две трети экрана — теперь там будет картинка
        image_layout = FloatLayout(
            size_hint=(1, 2 / 3),
            pos_hint={"top": 2 / 3}           
        )
               
        # Загружаем изображение из файла
        img = Image(source='Pic.png', allow_stretch=True, keep_ratio=False)
        image_layout.add_widget(img)

        # Кнопки по углам канваса
        button_easy = Button(
            text="Простой вопрос",
            pos_hint={"top": 0.91, "right": .4},
            size_hint=(0.4, 0.35)                   
        )
        
        button_hard = Button(
            text="Сложный вопрос",
            pos_hint={"top": .91, "right": 1},
            size_hint=(0.4, 0.35),
                   )
        
        button_incorrect = Button(
            text="Нет",
            pos_hint={"top": .5, "right": .4},
            size_hint=(0.4, 0.35),
        )

        button_correct = Button(
            text="Верно",
            pos_hint={"right": 1, "top" : .50},
            size_hint=(0.4, 0.35),
        )

        button_centr = Button(
            text="[b]Финальный вопрос[/b]",markup = True,            
            pos_hint={"right": .62, "top" : .90},
            size_hint=(0.23, 0.7),           
            background_color = (1,1,1,0.02),
            font_size = 20,
            color = (.73,.55,.5,1)            
        )
       
        button_correct.background_color = button_incorrect.background_color = button_easy.background_color = button_hard.background_color = (1,1,1,0.02)
        button_correct.font_size = button_incorrect.font_size = button_easy.font_size = button_hard.font_size = 20
        button_correct.color = button_incorrect.color = button_easy.color = button_hard.color = (.43,.58,.73,1)
        
        self.text_widget.bind(on_touch_down = self.label_touch)

        button_correct.bind(on_press=self.play_sound)
        button_incorrect.bind(on_press=self.play_sound)
        button_easy.bind(on_press=self.play_sound)
        button_hard.bind(on_press=self.play_sound)
        button_centr.bind(on_press=self.play_sound) 

        button_centr.soundfile = '..\music\q.mp3'
        button_hard.soundfile = '..\music\q_clock1.mp3'
        button_easy.soundfile = "..\music\clock.mp3"
        button_correct.soundfile = "..\music\q_correct1.mp3"
        button_incorrect.soundfile = "..\music\q_wrong.mp3"

        # предложения при нажатии кнопки
        button_centr.myText = ("Финальный вопрос, сектор приз на барабане!(поправил несуществующие усы)!","Дерзайте!")
        button_hard.myText = ("Время пошло!", "Время на обдумывание пролетело! Каков Ваш ответ?")
        button_easy.myText = ("Время пошло!", "Время на обдумывание вышло! Каков Ваш ответ?")
        button_correct.myText = ('И это правильный ответ!',"Кто бы мог подумать, но это верный ответ!","Вы поражаете меня своими познаниями", "Правильно!","Поздравляю, вы ответили правильно!")
        button_incorrect.myText =("Нет!","Хорошенько подумай и попробуй еще раз","Неправильно", "Учи матчасть!", "Повторяй теорию")
        
        # Добавляем компоненты в основную структуру
        self.up_layout = FloatLayout(
            pos_hint={"top": 1}                    
        )
         # Добавляем кнопки в макет с изображением
        image_layout.add_widget(button_easy)
        image_layout.add_widget(button_hard)
        image_layout.add_widget(button_incorrect)
        image_layout.add_widget(button_correct)
        image_layout.add_widget(button_centr)
       
        self.up_layout.add_widget(self.text_widget)
        self.main_layout.add_widget(self.up_layout)
        self.main_layout.add_widget(image_layout)
        root.add_widget(self.main_layout)
        
        return root

    # Воспроизведение мелодии, запуск таймера, запуск добавления окна таймера и удаление
    def play_sound(self, instance):
        
        self.myText = instance.myText # список выводов кнопки

        if self.sound is not None and self.sound.state == 'play':            
            self.sound.stop()       
            self.sound.unbind(on_stop=self.on_stop)           
            self.sound = None
        
        # Подгружаем музыкальный файл 
        ### СНАЧАЛО self.sound.stop() потом уже это все!!!
        self.sound_file_path = instance.soundfile
        self.sound = SoundLoader.load(self.sound_file_path)

        #Зацикливание звука через loop
        #self.sound.loop = True
        if  len(self.myText) == 2:      
            self.text_widget.text = self.myText[0] # изменение текста лейбла        
            self.button_porp = "create"             # изменение свойства (для создания кнопки)
            self.after_press_add()                  # запуск добавления кнопки
            self.start_timer(self.sound.length)     # запуск таймера 
            
        else:
            self.button_porp = "remove"
            self.after_press_add()
            self.text_widget.text = choice(self.myText)            
                                          
        if self.sound:
            self.sound.play()  # Начинаем воспроизведение
            #Регистрация события конца воспроизведения
            self.sound.bind(on_stop=self.on_stop)
   
    
    def on_stop(self,instance = def_instance):
        # если просто запустить change_text()  то при запуске звука сразу после первого машина посчитает,
        #  что остановка идет после воспроизведения и на лейбле будет сразу вторая фраза
        #FIXED  После переноса блока кода в def play стало работать нормально (видимо разнос
        #  между стоп и плей в несколько строчек кода сыграл свою роль (раньше они шли сразу друг
        #  за другом (порядок не поменялся))) Все равно оставлю это здесь на всякий...
        #Clock.schedule_once(self.change_text, 0.5)
        self.change_text()
    
    def change_text(self):   
        if len(self.myText) == 2 and self.sound.state != 'play':
            self.text_widget.text = self.myText[1]   


    #добавляем кнопку/удаляем кнопку, меняем свойство, рисуем круг (канвас под кнопкой(прозрачной)) 
    def after_press_add(self):

        if self.button_porp == "create" and self.after_press_right == None :
            self.after_press_right = Button(                
                text = '[b]___[/b]',markup = True,
                size_hint = (0.5/4,1/3),
                pos_hint = {'top': 1, "right":1},
                background_color=(.19, .55, .90, 0),
                background_normal ='',                
                font_size = 20                
                                            )
            
            with self.after_press_right.canvas.before:
                Color(rgba=(.17, .39, .65, 2))
                # Рисуем эллипс (круг)
                self.ellipse = Ellipse(size=self.after_press_right.size, pos=self.after_press_right.pos)

            self.after_press_right.bind(pos=self.update_el, size=self.update_el)
            
            self.text_widget.size_hint = (2/3, 1 / 3)
            self.up_layout.add_widget(self.after_press_right)

        elif self.button_porp == "remove" and self.after_press_right:
            
            self.timer_event.cancel() #остановка таймера

            self.up_layout.remove_widget(self.after_press_right) 
            self.text_widget.size_hint = (1, 1 / 3)
            self.after_press_right = None
            self.button_porp = 'wait'

    # логика таймера
    def start_timer(self, duration):
        """Запустить таймер"""
        self.duration = duration
        if not self.timer_event:
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)  # Обновление состояния каждые одну секунду
        else:
            self.timer_event.cancel()   # Перезапуск таймера при повторном нажатии
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self,dt):
       #Обновлять состояние таймера каждую секунду        
        if self.duration > 0:
            self.after_press_right.text =f'[b]{str(int(self.duration))}[/b]'  # Отображаем текущее значение таймера (markup в блоке объявления кнопки)
            self.duration -= 1
        else:
            Clock.unschedule(self.update_timer)  # Остановить обновляющий таймер
            self.after_press_right.text = 'Время вышло!'  # Сообщение о завершении таймера
    
    #TODO добавить смену кнопок при нажатии на лейбл
    def label_touch(self,touchX,touchY):
        pass
    
    def update_rectangle_main(self, instance, value):
        #Обновляет размер и позицию прямоугольника общего окна
        self.background_rect.pos = instance.pos
        self.background_rect.size = instance.size

    def update_el(self, instance, value):
    #Перемещение круга под таймер 
        self.ellipse.pos = instance.pos
        self.ellipse.size = instance.size   

if __name__ == "__main__":
    QuizApp().run()
