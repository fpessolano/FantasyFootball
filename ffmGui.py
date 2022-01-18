"""
ffmGUI.py: GUI game
"""

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from gui.startgame import *
from gui.newgame import *
from gui.season import *
from kivy.uix.screenmanager import ScreenManager, SwapTransition

Builder.load_file('kyvy_templates/ffm.kv')

Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '1080')


class SplashScreen(Screen):
    def switch(self, *args):
        self.manager.current = 'start_screen'

    def on_enter(self, *args):
        Clock.schedule_once(self.switch, 5)


class FantasyManager(ScreenManager):
    pass


class FantasyManagerApp(App):
    def build(self):
        return FantasyManager(transition=SwapTransition())


if __name__ == '__main__':
    FantasyManagerApp().run()
