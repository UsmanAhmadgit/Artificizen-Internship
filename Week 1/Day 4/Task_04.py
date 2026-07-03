#4. Write a class with a private attribute, exposing it safely through @property.

class Player:
    def __init__(self, username, starting_score=0):
        self.username = username
        self.__score = starting_score 

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_score):
        if new_score < 0:
            print("System: Score cannot drop below 0! Setting to 0.")
            self.__score = 0
        elif new_score > 9999:
            print("System: Max score reached! Setting to 9999.")
            self.__score = 9999
        else:
            self.__score = new_score

player1 = Player("Usman", 100)

player1.score = 500
print(f"Current Score: {player1.score}")  

player1.score = -50  
print(f"Current Score: {player1.score}")  

player1.score = 50000 
print(f"Current Score: {player1.score}")  