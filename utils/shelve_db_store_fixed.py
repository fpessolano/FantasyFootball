"""
Fixed version of shelve_db_store that properly handles nested dictionary updates
"""
import shelve
import time
from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class GameData:
    """
    Fixed version that properly handles shelve's nested dictionary limitation
    """
    
    def __init__(self, user_id='system', savefile='gamesaves'):
        self.__db = shelve.open(savefile)
        self.__id = user_id
        if user_id not in self.__db:
            self.__db[user_id] = {'saved_games': {}, 'last_login': int(time.time())}
        else:
            # Update last login - this forces shelve to detect changes
            user_data = self.__db[user_id]
            user_data['last_login'] = int(time.time())
            self.__db[user_id] = user_data
    
    def save_game(self, name, state, force=True):
        """Fixed save_game that properly updates shelve database"""
        if not self.__id:
            return False
            
        state = JsonEncoder().encode(state)
        
        # Fix: Read entire user record, modify it, write it back
        user_data = self.__db[self.__id]
        
        if not force and name in user_data['saved_games']:
            return False
            
        user_data['saved_games'][name] = state
        
        # This is the key fix - reassign the entire record
        self.__db[self.__id] = user_data
        
        # Ensure changes are written to disk
        self.__db.sync()
        
        return True
    
    def read_game(self, name):
        if not self.__id:
            return None
        user_data = self.__db.get(self.__id, {})
        saved_games = user_data.get('saved_games', {})
        return saved_games.get(name)
    
    def saved_game_list(self):
        if not self.__id:
            return []
        user_data = self.__db.get(self.__id, {})
        return list(user_data.get('saved_games', {}).keys())
    
    def delete_saved_game(self, name):
        """Fixed delete that properly updates shelve"""
        if not self.__id:
            return False
            
        user_data = self.__db[self.__id]
        if name in user_data['saved_games']:
            del user_data['saved_games'][name]
            self.__db[self.__id] = user_data
            self.__db.sync()
            return True
        return False
    
    def save_state(self, name, state, force=True):
        if not self.__id:
            return False
            
        user_data = self.__db[self.__id]
        
        if not force and name in user_data:
            return False
            
        user_data[name] = state
        self.__db[self.__id] = user_data
        self.__db.sync()
        
        return True
    
    def read_state(self, name):
        if not self.__id:
            return None
        user_data = self.__db.get(self.__id, {})
        return user_data.get(name)
    
    def state_list(self):
        if not self.__id:
            return []
        user_data = self.__db.get(self.__id, {})
        states = list(user_data.keys())
        if 'saved_games' in states:
            states.remove('saved_games')
        return states
    
    def delete_state(self, name):
        if not self.__id:
            return False
            
        user_data = self.__db[self.__id]
        if name in user_data:
            del user_data[name]
            self.__db[self.__id] = user_data
            self.__db.sync()
            return True
        return False
    
    def kill(self):
        if not self.__id:
            return
        if self.__id in self.__db:
            del self.__db[self.__id]
            self.__db.sync()
    
    def __del__(self):
        self.__db.close()
    
    @classmethod
    def clean(cls, maximum_age_hours=480):
        """Clean old unused profiles"""
        import time
        current_time = int(time.time())
        max_age_seconds = maximum_age_hours * 3600
        
        with shelve.open('gamesaves') as db:
            users_to_delete = []
            
            for user_id in db.keys():
                user_data = db.get(user_id, {})
                last_login = user_data.get('last_login', 0)
                
                if current_time - last_login > max_age_seconds:
                    users_to_delete.append(user_id)
            
            for user_id in users_to_delete:
                del db[user_id]
                
            if users_to_delete:
                db.sync()
                print(f"Cleaned {len(users_to_delete)} old profiles")