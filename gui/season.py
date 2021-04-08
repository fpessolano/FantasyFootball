from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('kyvy_templates/season.kv')


class SeasonPlay(Screen):
    testData = 'nothing'

    def __init__(self, **kwargs):
        super(SeasonPlay, self).__init__(**kwargs)

    def load_game_data(self, data):
        # TODO
        print(data)

    def quit(self):
        print(self.testData)
        quit()
