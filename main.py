from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

import os

# Kitoblar ro‘yxatini avtomatik o‘qish (2 ta hozircha)
kitoblar = {
    "Oltin Nasihatlar": {"text": "txt/tt.txt", "audio": "aud/aa.mp3"},
    "Payg‘ambarlar Qissasi": {"text": "text/2.txt", "audio": "audio/2.mp3"}
}

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        for nom, yol in kitoblar.items():
            btn = Button(text=nom, size_hint_y=None, height=60, on_press=self.och_kitob)
            layout.add_widget(btn)
        self.add_widget(layout)

    def och_kitob(self, instance):
        App.get_running_app().root.current = "kitob"
        App.get_running_app().root.get_screen("kitob").korsat(instance.text)

class KitobScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.label = Label(text="", size_hint_y=0.7)
        
        self.btn_play = Button(text="Eshitish", size_hint_y=0.1, on_press=self.oyinla)
        self.btn_pause = Button(text="Pauza", size_hint_y=0.1, on_press=self.pauza)
        self.btn_stop = Button(text="To‘xtatish", size_hint_y=0.1, on_press=self.toxtat)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn_play)
        self.layout.add_widget(self.btn_pause)
        self.layout.add_widget(self.btn_stop)

        self.add_widget(self.layout)
        self.sound = None
        self.audio_file = ""

    def korsat(self, nom):
        fayl = kitoblar[nom]['text']
        if os.path.exists(fayl):
            with open(fayl, 'r', encoding='utf-8') as f:
                self.label.text = f.read()
        self.audio_file = kitoblar[nom]['audio']
        if self.sound:
            self.sound.stop()
        self.sound = SoundLoader.load(self.audio_file)

    def oyinla(self, instance):
        if self.sound:
            self.sound.play()

    def pauza(self, instance):
        if self.sound:
            self.sound.stop()  # Kivyda pause yo‘q, stop qilib keyin `.seek()` bilan qaytish mumkin
            print("Pauza bosildi (ammo bu to‘xtatishga teng)")

    def toxtat(self, instance):
        if self.sound:
            self.sound.stop()
            print("Audio to‘xtatildi")

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(KitobScreen(name="kitob"))
        return sm

if __name__ == "__main__":
    MyApp().run()
