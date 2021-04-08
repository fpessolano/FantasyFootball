from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from support.diskstore import SaveFile

Builder.load_file('kyvy_templates/startgame.kv')


class StartGame(Screen):
    def __init__(self, **kwargs):
        super(StartGame, self).__init__(**kwargs)
        self.saveFile = SaveFile("saves.dat")
        Clock.schedule_once(self.add_button, 1)

    def callback(self, saved_game):
        saved_game = self.saveFile.read_state(saved_game.text)
        if not saved_game:
            return
        self.manager.screens[3].load_game_data(saved_game)
        self.manager.current = 'season_screen'

    def add_button(self, *args):
        saved_games = self.saveFile.stateList()
        for saved_game in self.saveFile.stateList():
            btn = Button(text=f'{saved_game}', font_size=24, background_color=[0, .7, .4, .85])
            btn.bind(on_press=self.callback)
            self.ids.saveGame.add_widget(btn)
        if len(saved_games) < 6:
            for i in range(6 - len(saved_games)):
                btn = Button(text=f'empty', font_size=24, background_color=[0.7, 0, 0, 0.7] )
                self.ids.saveGame.add_widget(btn)

    def new_game(self):
        self.manager.current = 'new_screen'
