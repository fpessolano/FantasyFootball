import pickle


class SaveFile:
    """
    This class manages loading and saving save files
    """

    def __init__(self, filename):
        self.__filename = filename
        try:
            infile = open(self.__filename, 'rb')
            self.__savedState = pickle.load(infile)
            infile.close()
        except:
            self.__savedState = {}

    def writeState(self, nameState, state):
        self.__savedState[nameState] = state
        outfile = open(self.__filename, 'wb')
        pickle.dump(self.__savedState, outfile)
        outfile.close()
        return True

    def readState(self, nameState):
        try:
            if len(self.__savedState) == 0:
                infile = open(self.__filename, 'rb')
                self.__savedState = pickle.load(infile)
                infile.close()
                return self.__savedState[nameState]
            else:
                return self.__savedState[nameState]
        except:
            return None

    def stateList(self):
        return self.__savedState.keys()

    def deleteState(self, nameState):
        try:
            del self.__savedState[nameState]
            outfile = open(self.__filename, 'wb')
            pickle.dump(self.__savedState, outfile)
            outfile.close()
        except:
            return False
        return True
