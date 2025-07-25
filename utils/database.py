import pickle


class SaveFile:
    """
    This class manages loading and saving save files
    """

    def __init__(self, filename):
        self.__filename = filename
        try:
            infile = open(self.__filename, 'rb')
            self.__saved_state = pickle.load(infile)
            infile.close()
        except:
            self.__saved_state = {}

    def write_state(self, nameState, state):
        self.__saved_state[nameState] = state
        outfile = open(self.__filename, 'wb')
        pickle.dump(self.__saved_state, outfile)
        outfile.close()
        return True

    def read_state(self, nameState):
        try:
            if len(self.__saved_state) == 0:
                infile = open(self.__filename, 'rb')
                self.__saved_state = pickle.load(infile)
                infile.close()
                return self.__saved_state[nameState]
            else:
                return self.__saved_state[nameState]
        except:
            return None

    def stateList(self):
        return self.__saved_state.keys()

    def deleteState(self, nameState):
        try:
            del self.__saved_state[nameState]
            outfile = open(self.__filename, 'wb')
            pickle.dump(self.__saved_state, outfile)
            outfile.close()
        except:
            return False
        return True
