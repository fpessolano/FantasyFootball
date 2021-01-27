from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

Builder.load_file('kyvy_templates/startgame.kv')

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