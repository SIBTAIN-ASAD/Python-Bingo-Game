import urllib.request 
import random

"""
===================================================================
This Function is used to load the data from the given URL
===================================================================
"""
def readFromURL(url, list_items):
    response = urllib.request.urlopen(url) 
    html= response.readline() #reads one line

    while len(html) != 0: # while there are still lines remaining in the file
        data =  html.decode('utf-8').strip() # strip() this line and add into a list of "tokens"

        list_items.append(data)
        html= response.readline() #reads the next line


    return (list_items)

"""
===================================================================
This Function is used to make a dictionary of players 
The dictionary will have players' names as key and respected 2D list 
pattern of unque items
===================================================================
"""
def initialtePlayers(list_items):
    dic = {}
    num = input("How many players want to play game: ")
    
    while(num.isdigit() == False or int(num) <= 0 or int(num) > 5):
        num = input("Please enter a valid number (1 - 3): ")
    
    for i in range(int(num)):
        name = input(f"Enter the name of player {i+1}: ")
        while name in dic:
            name = input(f"Name is Already in game. Plese enter the unique name of player {i+1}: ")
        
        ls = []
        ls2 = []
        k = 0
        while(k < 25):
            idx = random.randrange(len(list_items))
            ran = list_items[idx]
            if ran not in ls2:           
                ls2.append(ran)
                k += 1
            if k%5 == 0:
                ls.append(ls2)
                ls2 = [] 
        dic[name] = ls
                    
    return dic

"""
===================================================================
This Function is used to display the name and card of the passed 
player key , using dictionary
===================================================================
"""
def displayPlayerCard(dic, name):
    print("--------------------------------------")
    print(f"\n{name}'s Card\n")
    for i in range(5):
        for j in range(5):
            print("{:30s}".format(dic[name][i][j]), end = "")
        print("")


"""
===================================================================
This Function is used to display all players 
(calling displayPlayerCard function)
===================================================================
"""
def displayAll(dic):
    for i in dic:
        displayPlayerCard(dic, i)



"""
===================================================================
This Function is used to check winner on the FULL CARD mode 
===================================================================
"""
def isFullCardWinner(dic, name):
    for i in range(5):
        for j in range(5):
            if dic[name][i][j] != "FOUND":
                return False
    return True

"""
===================================================================
This Function is used to check winner on the Single Line mode 
===================================================================
"""
def isSingleLineWinner(dic, name):
    # checking left diagonal
    ls = []
    check = True
    for i in range(5):
        for j in range(5):
            if i == j:
                ls.append(dic[name][i][j])
    for i in ls:
        if i != "FOUND":
            check = False
    if check == True:
        return True


    # checking right diagonal
    ls = []
    check = True
    for i in range(5):
        for j in range(5):
            if i != j and i+j == 4:
                ls.append(dic[name][i][j])
    for i in ls:
        if i != "FOUND":
            check = False
    if check == True:
        return True

    # checking rows
    for k in range(5):
        ls = []
        check = True
        for i in range(5):
            for j in range(5):
                if i == k:
                    ls.append(dic[name][i][j])
        for i in ls:
            if i != "FOUND":
                check = False
        if check == True:
            return True

    # checking columns
    for k in range(5):
        ls = []
        check = True
        for i in range(5):
            for j in range(5):
                if j == k:
                    ls.append(dic[name][i][j])
        for i in ls:
            if i != "FOUND":
                check = False
        if check == True:
            return True

    return False


"""
===================================================================
This Function is used to check winner on the Four Corner mode 
===================================================================
"""
def isFourCornersWinner(dic, name):
    ls = []
    for j in range(5):
        ls.append(dic[name][0][j])
    for j in range(5):
        ls.append(dic[name][4][j])
    for i in range(5):
        ls.append(dic[name][i][0])
    for i in range(5):
        ls.append(dic[name][i][4])

    for i in ls:
        if i != "FOUND":
            return False
    return True

    


"""
===================================================================
This Function is used to check winner
Basically this function calles the respected function using 
mode value
===================================================================
"""
def checkWinner(inp, dic, name):
    if inp == 1:
        return isFullCardWinner(dic, name)
    elif inp == 2:
        return isSingleLineWinner(dic, name)
    elif inp == 3:
        return isFourCornersWinner(dic, name)
    else:
        False

"""
===================================================================
This Function is used to get mode entered by the player 
===================================================================
"""
def getGameMod():
    print("\nPress 1 for Full Card (all items on the card must be FOUND)")
    print("Press 2 for Single Line (all items in a single horizontal or vertical line must be marked as FOUND)")
    print("Press 3 for Four Corners (the items in each of the four corners of the card must be FOUND) ")
    inp = input()
    if inp == "1":
        return 1
    elif inp == "2":
        return 2
    elif inp == "3":
        return 3
    else:
        print("Invalid Input, mod 1 is selected")
        return 1
    

"""
===================================================================
This Function is used to get a new random item for the caller 
===================================================================
"""
def getNewItemForCaller(list_items, list_caller):
    k = 0
    while(k < 300):
        idx = random.randrange(len(list_items))
        ran = list_items[idx]
        if ran not in list_caller:           
            list_caller.append(ran)
            return list_caller


"""
===================================================================
This Function is used to set all the players found item to FOUND
===================================================================
"""
def removeItemFromPlayersCards(dic, item):
    for k in dic:
        for i in range(5):
            for j in range(5):
                if dic[k][i][j] == item:
                    dic[k][i][j] = "FOUND"



"""
===================================================================
This Function is used to display the winners in case of winnings
===================================================================
"""
def endTheGame(dic, winners):
    print("\n-----------------------------")
    print("*        Game End           *")
    print("-----------------------------")
    print("Winners are")
    for i in winners:
        print(i)
    for i in winners:
        displayPlayerCard(dic, i)



"""
===================================================================
This Function is used to run the game , called by main program

This function do
1. Initialize players
2. get mode
3. display players
4. run game logic
===================================================================
"""
def Game(list_items):

    print("\n=============================")
    print("|       BINGO GAME          |")
    print("=============================\n")

    # populating user cards
    dic = initialtePlayers(list_items)

    # Asking to know the mode of winning
    mode = getGameMod()

    # displaying Cards
    displayAll(dic) 

    # list of called items
    caller_list = []
    print("\n-----------------------------")
    print("      GAME HAS STARTED")
    print("-----------------------------\n")
    
    while True:
        # Asking player choice
        print("<= Enter P key to ask CALLER to tell item =>")
        print("<= Enter S key to display cards =>")
        inp = input()

        # input validation
        while inp != "p" and inp != "P" and inp != "S" and inp != "s":
            inp = input("Please Enter a valid input: ")

        # get new item and replace player's data's item by FOUND 
        if inp == "P" or inp == "p":
            caller_list = getNewItemForCaller(list_items,caller_list)
            item = caller_list[-1]

            removeItemFromPlayersCards(dic, item)

            # list to store winners
            winners = []

            for i in dic:
                if checkWinner(mode, dic, i) == True:
                    winners.append(i)

            # check for winners
            if len(winners) > 0:
                endTheGame(dic, winners)
                return None
        else:
            displayAll(dic)


"""
===================================================================
This Function is used to call game and ask again and again from
user to play again or not 
===================================================================
"""
def main():
    # list to store items
    list_items = []

    # getting data from URL
    readFromURL("https://research.cs.queensu.ca/home/cords2/bingo.txt", list_items)

    inp = "Y"
    while inp == "Y" or inp == "y":
        Game(list_items)
        inp = input("Do you want to play again (Y/N): ")



# calling main function
if __name__ == "__main__":
    main()
