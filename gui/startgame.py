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
        Clock.schedule_once(self.addButton, 1)

    def callback(self, savedGame):
        savedGame = self.saveFile.readState(savedGame.text)
        if not savedGame:
            return
        self.manager.screens[3].loadGameData(savedGame)
        self.manager.current = 'season_screen'

    def addButton(self, *args):
        savedGames = self.saveFile.stateList()
        for savedGame in self.saveFile.stateList():
            btn = Button(text=f'{savedGame}', font_size=24)
            btn.bind(on_press=self.callback)
            self.ids.saveGame.add_widget(btn)
        if len(savedGames) < 6:
            for i in range(6-len(savedGames)):
                btn = Button(text=f'empty', font_size=24)
                self.ids.saveGame.add_widget(btn)

    def newGame(self):
        self.manager.current = 'new_screen'