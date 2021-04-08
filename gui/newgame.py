from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('kyvy_templates/newgame.kv')


class CreateNewGame(Screen):
    def create_game(self):
        self.manager.current = 'season_screen'

    def go_back(self):
        self.manager.current = 'start_screen'