from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition

Builder.load_file('frontend.kv')


class SeasonPlay(Screen):
    def quit(self):
        quit()


# for some reason layout is not working, takes only a small part of the screen !!!
class CreateNewGame(Screen):
    def createGame(self):
        self.manager.current = 'season_screen'

    def goBack(self):
        self.manager.current = 'start_screen'


class StartGame(Screen):
    def __init__(self, **kwargs):
        super(StartGame, self).__init__(**kwargs)
        Clock.schedule_once(self.addButton, 1)

    def addButton(self, *args):
        for i in range(5):
            # see how toi add on_press and/or id
            # set font size to 18
            self.ids.saveGame.add_widget(Button(text=f'SaveGame{i}'))

    def newGame(self):
        self.manager.current = 'new_screen'


class FantasyManager(ScreenManager):
    pass


class FantasyManagerApp(App):
    def build(self):
        return FantasyManager(transition=SwapTransition())


if __name__ == '__main__':
    FantasyManagerApp().run()
