import sys
import time

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from game.team import Team

Builder.load_file('kyvy_templates/season.kv')


class StandingsRow(BoxLayout):
    # todo proper method for initialisation and modification
    def __init__(self, team: Team):
        super(StandingsRow, self).__init__()
        data = team.data()
        self.ids.name.text = data['NAME']
        self.ids.mp.text = str(data['MP'])
        self.ids.w.text = str(data['W'])
        self.ids.d.text = str(data['D'])
        self.ids.l.text = str(data['L'])
        self.ids.gf.text = str(data['GF'])
        self.ids.ga.text = str(data['GA'])
        self.ids.gd.text = str(data['GD'])
        self.ids.pt.text = str(data['PT'])




class SeasonPlay(Screen):

    def __init__(self, **kwargs):
        super(SeasonPlay, self).__init__(**kwargs)
        self.minimum_height = 30
        self.rows = []

    def load_game_data(self, data):
        # TODO
        try:
            for team in data['teams']:
                # self.rows.append(self.ids.standings.add_widget(Row()))
                self.ids.standings.add_widget(StandingsRow(team))
            print(data)
        except:
            print ("Unexpected error:", sys.exc_info()[0])

    def quit(self):
        quit()
