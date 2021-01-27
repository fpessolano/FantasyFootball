from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('kyvy_templates/season.kv')


class SeasonPlay(Screen):
    def quit(self):
        quit()
