from modules.ffm import FFM

def playGame():
    print("Welcome to FMM2021")
    print("Version 0.2.0\n")

    game = FFM()

    command = ""
    while True:
        while command != "n" and command != "l":
            command = input("(N)ew game or (L)oad game? ").lower()
            if command != "n" and command != "l":
                print("!!! ERROR: please write a valid command !!!")
        if command == "l":
            game.load()
            break
        else:
            while not game.new():
                print('Failed to create league.', end=' ')
                tryAgain = input("Try again (y for yes)? ").lower()
                if tryAgain != 'y':
                    print("Bye Bye!")
                    quit()
            break

    while True:
        game.playRound()

        if input("\nPlay again with the same teams (y/n)? ").lower() != "y":
            game.end()
            break

    print("\nThanks for playing!")


if __name__ == '__main__':
    playGame()
