from replit import db
import time

# TODO move from a file to the database, need separation between save games and generic game data


class GameData:
    """
    This class manages loading and saving save files
    """
    def __init__(self, user_id='system'):
        self.__id = user_id
        if user_id not in db:
            db[user_id] = {'saved_games': {}, 'last_login': int(time.time())}
        else:
            db[user_id]['last_login'] = int(time.time())

    def save_game(self, name, state, force=True):
        if not self.__id:
            return False
        if not force and name in db[self.__id]['saved_games']:
            return False
        db[self.__id]['saved_games'][name] = state
        return True

    def read_game(self, name):
        if not self.__id:
            return None
        if name in db[self.__id]['saved_games']:
            return db[self.__id]['saved_games'][name]
        return None

    def saved_game_list(self):
        if not self.__id:
            return
        return list(db[self.__id]['saved_games'].keys())

    def delete_saved_game(self, name):
        if not self.__id:
            return
        if name in db[self.__id]['saved_games']:
            del db[self.__id]['saved_games'][name]

    def save_state(self, name, state, force=True):
        if not self.__id:
            return False
        if not force and name in db[self.__id]:
            return False
        db[self.__id][name] = state
        return True

    def read_state(self, name):
        if not self.__id:
            return None
        if name in db[self.__id]:
            return db[self.__id][name]
        return None

    def state_list(self):
        if not self.__id:
            return
        states = list(db[self.__id].keys())
        states.remove('saved_games')
        return states

    def delete_state(self, name):
        if not self.__id:
            return
        if name in db[self.__id]:
            del db[self.__id][name]

    def kill(self):
        if not self.__id:
            return
        del db[self.__id]

    @classmethod
    def clean(cls, maximum_age_hours=480):
        # TODO to be done
        pass


if __name__ == '__main__':
    test = GameData('ciao')
    print(db.keys())
    test.save_game('test', 1)
    print(test.read_game('test'))
    print(test.saved_game_list())
    test.save_state('test', 1)
    print(test.state_list())
    print(test.read_state('last_login'))
    test.kill()

    print(db.keys())
