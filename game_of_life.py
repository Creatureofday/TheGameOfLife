# Creator:      Jack Carter
# Contact:      jackcart@usc.edu
# Date Created: 12/09/2022
# Modified:     02/22/2023 (extended comments and corrected several edge conditions / infinite loops)
# Description:  This is a simplified rendition of the classic board game, "The Game of Life." This was a class project for an introductory
#               python course that asked us to create any project we wanted to that included several of the techniques we learned in class
#               such as object oriented programming, lists, loops, functions, etc. There may be edge cases not considered, and the UI
#               is quite clunky, but it was my first time attempting to code a larger project in Python.

import random
import numpy as np

CAREER = DISP_INFO = ADD_PLAYER = '1'
EDUCATION = MOVE = REMOVE_PLAYER = '2'
PASS = '3'
SHOW_YOUR_MAP = '4'
EXIT = '0'
END = "X"
DIVIDER = '\n--------------------------------------\n'

####################
# Player Conditions
####################
player_list = []

####################
# Board Conditions
####################
ROWS = 2
COLUMNS = 18

# game length
END_OF_GAME = (ROWS*COLUMNS)

# this initializes a "visualization" of the board state
board = np.full((ROWS,COLUMNS), '_', str)
ACTION_POSITIONS = [5,6,10,13,20,30]

# this refers to the different action tiles on the board
class Event:
    def __init__(self,name: str, locations: list[int], symbol: str):
        self.name = name
        self.positions = locations
        self.symbol = symbol

# these are all action tiles
PAY_SQUARE = Event("Paycheck", [6 ,10, 14, 18, 22, 26, 30], '$')
CAREER_CHANGE = Event("Career Change", [12, 24], "@")
EDUCATION_CHANCE = Event("Education Chance", [17], "?")
RELATIONSHIP = Event("Love Interest", [4, 13, 23, 31], '!')
CHILDREN = Event("Children", [7, 16, 25], "<")

# used during the board initialization
LIST_OF_EVENTS = [PAY_SQUARE, CAREER_CHANGE, EDUCATION_CHANCE, RELATIONSHIP, CHILDREN]

# creates a set of all the different action tiles
ALL_EVENT_SQUARES = set().union(
    PAY_SQUARE.positions,
    CAREER_CHANGE.positions,
    EDUCATION_CHANCE.positions,
    RELATIONSHIP.positions,
    CHILDREN.positions
)

# this is in reference to the 3 included careers a player can have
class Career:
    def __init__(self, career_name: str, base_salary: int, description: str):
        self.name = career_name
        self.salary = base_salary
        self.description = description
    
    def print_name(self) -> str:
        return self.name    
        
    # allows for a given career to be called as though it were a string, and return it's key characteristics
    def __str__(self) -> str:
        return (
            self.name + '\n' + 'Salary: $'+ str(self.salary) + '\n' + self.description
        )

# these are the included careers
ARTIST = Career("Artist", 30000, "An artist has a very low base pay")
PLUMBER = Career("Plumber", 60000,"A plumber has a basic salary")
UNEMPLOYED = Career("Unemployed", 0, "This is the start of everything, only way is up")
career_list = [ARTIST, PLUMBER]

# in reference to the 4 different education levels achievable in the game
class Education: 
    def __init__(self, type_of_education: str, bonus: float, cost: int):
        self.name = type_of_education
        self.bonus = bonus
        self.cost = cost
    
    def full_info(self) -> str:
        return (
            self.name + '\n' + f"({self.name} multiplies your salary by {1.0 + self.bonus})"
        )
    
    def __str__(self) -> str:
        return self.name
        
COMMUNITY_COLLEGE = Education("Community College", 0.2, 20000)
STATE_UNIVERSITY = Education("University", 0.6, 50000)
GRADUATE_SCHOOL = Education("Graduate School", 1.0, 90000)
GED = Education("GED", 1.0, 0)

education_list = [COMMUNITY_COLLEGE, STATE_UNIVERSITY, GRADUATE_SCHOOL]

class Player:
    # initialize the player and attributes
    def __init__(self, player_name: str):
        self.name = player_name
        # starting balance
        self.balance = 100000
        self.kids = 0
        # GED = basic, everyone starts with atleast this
        self.education = [GED]
        # will be changed based on player start
        self.career = UNEMPLOYED
        self.retired = False
        # once a player gets set up this changes
        self.initialized = False
        self.position = 0
        # this is the character that will mark the player on the map
        self.character = ''
        #boolean if they're married or not
        self.married = False
        #ask players if they want to start with a college or career path
        #self.starting_path = ''
        self.total_bonus = 1.0
    
    # WILL replace when the education is added, to avoid double counting
    # This will calculate the total bonus 
    def calc_education_bonus(self) -> None:
        for education in self.education:
            self.total_bonus =+ education.bonus
            
    # this moves the player the given distance
    def move(self, distance: int) -> None:
        
        # if the player would go past the end of the game...
        if (self.position + distance >= END_OF_GAME):
            # instead set their position to the last tile
            self.position = END_OF_GAME
            # set them to retired...
            self.retired = True
            print(f"{self.name} has reached the end of the game!\n")
        # if they would not move past the end of the game...
        else:
            # move them the appropriate distance
            self.position += distance
            print(f"{self.name} has reached position {self.position}\n")
    
    # print all relevent information about the player
    def full_info(self) -> None:
        print(
            f'Player: {self.name}\n' +
            f'Balance: {self.balance}\n' +
            f'Career: {self.career.name}\n' +
            f'Kids: {self.kids}\n' +
            f'Board Position: {self.position}'
        )
        print("Accreditations:")
        # print each of the academic achievements of the person
        for degree in self.education:
            print('\t' + degree.name)
            
        # handle the situation if they're married or not
        if self.married:
            print("Married")
        else:
            print("Unmarried")
    # print(f"\nAre you sure you want to start with the following players? {', '.join(initial_players)} ")    
    
    def pay(self) -> None:
        amount = int(self.career.salary * self.total_bonus)
        print(f"{self.name} has recieved ${amount}\n")
        self.balance += amount
    
    def spend(self, cost: int) -> None:
        self.balance -= cost
    
    # allows the Player to get called like a string (return the name)
    def __str__(self) -> str:
        return (self.name)   

# this will end the game if called and confirmed
def end_game() -> None:
    choice = input("Are you sure you would like to exit the game (input 'Y' or 'N')?\n").strip()
    while choice not in ['Y', 'N']:
        print("Invalid input\n")
        choice = input("Are you sure you would like to exit the game (input 'Y' or 'N')?\n").strip()
    
    # at this point, only X and Y should be options
    if choice == 'Y':
        print("Thank you for playing!\n")
        exit()
    else:
        print("Returning to game...\n")

# may want to impliment this option in the Player class
def move_player(target_player: Player) -> None:
    start_position = target_player.position
    input("Press any key to roll the die ")
    target_player.move(roll_die())
    end_position = target_player.position
    
    # this will handle if you hit any action square
    if any(x in ALL_EVENT_SQUARES for x in (list(range(start_position+1,end_position+1)))):
        # this will iterate through every square you passed while moving
        for passed_square in (list(range(start_position+1,end_position+1))):
            
            # handles if you hit a pay square during moving
            if passed_square in PAY_SQUARE.positions:
                if target_player.career != UNEMPLOYED:
                    print(f"{target_player} has recieved a paycheck!")
                    target_player.pay()
                else:
                    print("if you had a job, you would have gotten paid...")
                print(DIVIDER)
        
            # handles if you hit a Career Change square
            if passed_square in CAREER_CHANGE.positions:
                print("You've hit a Career Change square!")
                
                # draw a career card for the current player, if they're employed, they get a choice
                if target_player.career != UNEMPLOYED:
                    draw_career_card(target_player, True)
                    
                # draw a card and if the player is unemployed, they don't get a choice if they take the job
                else:
                    draw_career_card(target_player, False)
                print(DIVIDER)
                
            # handles if you hit an Education Change square
            if passed_square in EDUCATION_CHANCE.positions:
                print("You've hit an Education tile!")
                # draw a college card for the current player, with the option to pursue it (for a price)
                draw_college_card(target_player, True)
                print(DIVIDER)
        
            # handles if you hit a relationship square
            if passed_square in RELATIONSHIP.positions:
                print("You've hit a Romance opportunity tile!")
                handle_relationship(target_player)
                print(DIVIDER)
            
            # handles if you hit a children square
            if passed_square in CHILDREN.positions:
                print("You've ran into an opportunity to have children!")
                handle_children(target_player)
                print(DIVIDER)
    
# roll a single 6 sided die
def roll_die() -> int:
    min = 1
    max = 6
    print("Rolling die!")
    dice_roll = random.randint(min,max)
    print(str(dice_roll) + '!')
    
    return dice_roll

# roll to see if you are romantically successful
def handle_relationship(target_player: Player) -> None:
    
    # if the player is not currently married
    if not target_player.married:
        choice = input("Press 1 if you wish to attempt to get married (50%/ chance), press 2 otherwise: ")
        while choice not in ['1', '2']:
            choice = input("Please input valid response, 1 or 2: ")
    
        # if they want to attempt getting married
        if choice == '1':
            # generate a random boolena
            outcome = bool(random.getrandbits(1))
            # if they were successful in the marriage attempt
            if outcome == True:
                print("You got married!")
                target_player.married = True
            # if they were unsuccessful
            else:
                print("You were not successful!")
        # if they do not want to attempt getting married
        else:
            print("You passed up on the chance to get married")
    
    # if they are already married, they cannot try to marry again
    else:
        print("However, you are already married!")
        
    print(DIVIDER)

# handles the having children decision
def handle_children(target_player: Player) -> None:
    # min and max number of children
    min = 0
    max = 3
    # we only allow kids with married players
    if target_player.married:
        choice = input(
            f"Do you want to try for children (outcome {min}-{max})?\n" +
            "1: Yes\n" +
            "2: No" + '\n'
            )
        # this will ensure the choice is valid
        while choice not in ['1','2']:
            choice = input("Please enter a valid answer: 1 or 2")
        
        # if they want to have children...
        if choice == '1':
            outcome = random.randint(min,max)
            # if you have children...
            if outcome > 0:
                print(f"You had {outcome} kid(s)!")
                target_player.kids += outcome
            # if you do not have children...
            else:
                print("Unfortunately, you did not have any children this time")
        # if they do not want children...
        else:
            print("You chose not to try for children at this time")
    # if the player is unmarried
    else:
        print("Unfortunately, you are not married and don't feel comfortable having kids")
 
# draw a career card and handle the situation
def draw_career_card(active_player: Player, choice_to_pick: bool) -> None:
    print('\n' + DIVIDER)
    input("Press any key to draw your career card... ")
    print(DIVIDER)
    decision = '0'
    drawn_career = random.choice(career_list)
    print(f"You've drawn:\n{drawn_career}\n")
    if not choice_to_pick:
        active_player.career = drawn_career
        print(f'{active_player} is now a(n) {drawn_career.name}')
        
    else:
        # will handle if they dont already have this career
        if drawn_career != active_player.career:
            decision = input(f"Would you like to switch your career to {drawn_career.name}?\n1: Switch\n2: Keep\n")
            
            # this will run as long as they are not providing a valid response
            while decision not in ['1', '2']:
                decision = input("Please enter a valid option:\n1: Switch\n2: Keep")
        
            # if they choose to change careers...
            if decision == '1':
                active_player.career = drawn_career
                print(f"You've decided to switch to {active_player.career.name}")
            else:
                print(f"You've decided to stay a(n) {active_player.career.name}")
        # this will handle if they already have this career
        else:
            print(f"You already are a(n) {drawn_career.name}, so moving on!\n")
    
# draw a random college card
def draw_college_card(active_player: Player, choice_to_pick: bool) -> None:
    print(DIVIDER)
    input("Press any key to draw a college card... ")
    print(DIVIDER)
    decision = '0'
    drawn_college = random.choice(education_list)
    print(f"You've drawn\n{drawn_college.full_info()}")
    if not choice_to_pick:
        active_player.education.append(drawn_college)
        active_player.total_bonus += drawn_college.bonus
        print(f"{active_player} starts off having studied at {drawn_college.name}\n")
        
    else:
        decision = input(
            f"Would you like to recieve education at a {drawn_college.name}? It will cost ${drawn_college.cost}\n" +
            "(Note that these effects do compound and stack)\n" +
            "Press 1 if Yes, 2 if No: "
        )
        # this loop will ensure that the user puts in a valid answer
        while decision not in ['1','2']:
            decision = input("Please choose a valid answer:\n1: Change\n2:Keep")

        # if they decide to recieve the education
        if decision == '1':
            # add the education to their list of educations
            active_player.education.append(drawn_college)
            # the player spends the amount the education costs
            active_player.spend(drawn_college.cost)
            # this will update the player's education bonus
            active_player.total_bonus += drawn_college.bonus
            print(f"You've decided to recieve education at {drawn_college.name} and spent {drawn_college.cost}")
        else:
            print(f"You've decided to not to pursue further education\n")
            
# display the options a player has during their turn
def display_options() -> None:
    print(
        DIVIDER +
        f"{DISP_INFO}: Display Player Info\n" +
        f"{MOVE}: Move\n" +
        f"{PASS}: Pass your Turn\n" +
        f"{SHOW_YOUR_MAP}: Show your position on the map\n" +
        f"{END}: Exit and end the current game\n" +
        DIVIDER
        )

# brief display of the choices one has for their initial path
def display_starting_choices() -> None:
    print(
        f"{CAREER}: To start a career (and have only a GED to start)\n" +
        f"{EDUCATION}: To start college (and be unemployed to start)\n"
    )

# this will set the player up 
def player_creation(active_player: Player)-> None:
    character_choice = '?'
    while not character_choice.isalpha():
        character_choice = input("Choose a letter to represent your character: ").strip()
        if not character_choice.isalpha():
            print("Your choice must be a valid alphabet letter")
        else:
            active_player.character = character_choice
    display_starting_choices()
    start_choice = input("Choose the path you want to start: ")
    while start_choice not in [CAREER, EDUCATION]:
        display_starting_choices()
        start_choice = input(f"Please input either {CAREER} or {EDUCATION} to continue")
    # if they choose to start with a career
    if start_choice == CAREER:
        draw_career_card(active_player, False)

    # if they choose to start with college
    else:
        draw_college_card(active_player, False)
    
    print("You are now ready to begin your journey!")
    active_player.initialized = True
    
# this handles the actions a player chooses
def action_handler(player_list: list[Player] , active_player: int) -> None:
    curr_player = player_list[active_player]
    passed = False
    already_moved = False
    
    #once someone passes the turn, leave action menu
    while not passed:
        if not curr_player.retired:
            if curr_player.initialized:
                display_options()
                player_choice = input("Input action would you like to complete: ")
                print('\n')
                
                # handles if they want to display their info
                if player_choice == DISP_INFO:
                    curr_player.full_info()
                
                # handles if they want to move their player
                elif (player_choice is MOVE):
                    if(already_moved is False):
                        move_player(curr_player)
                        already_moved = True
                    else:
                        print("You've already moved!")
                
                # handles if they want to print the map
                elif player_choice == SHOW_YOUR_MAP:
                    print_board(board, curr_player)
                
                # handles if they want to pass their turn
                elif player_choice == PASS:
                    passed = True
                    
                elif player_choice == END:
                    end_game()
                
                # if no valid input given, announce
                else:
                    print("Not a valid choice")
            
            # this will be the start of a player's game, their choices
            else:
                player_creation(curr_player)
        
        # this occurs when a player has reached the end of the game, but they had not yet passed the turn
        else:
            print(
                f"You've reached the end of the game as a {curr_player.career.name} and retired with a balance of ${curr_player.balance}!\n" +
                f"You also had {curr_player.kids} kids!"
                )
            passed = True
    
    #this occurs at the end of a player's turn
    print("Passing the turn\n")
            
# potentially prints the board
def print_board(board: list[list[any]], curr_player: Player) -> None:
    
    # handle the placement of the players character at player's current position
    row = 0
    
    # if they are on a position that is greater than 18, snake them down a row on the map heading back to the left
    if curr_player.position > COLUMNS:
        row = 1
        location = ( curr_player.positon - 18 )
        old_symbol = board[row][-location]
        board[row][-location] = curr_player.character
    elif curr_player.position == 0:
        location = curr_player.position
        old_symbol = board[row][location]
        board[row][location] = curr_player.character
    else:
        location = curr_player.position
        old_symbol = board[row][location]
        board[row][location] = curr_player.character
    
    
    print(DIVIDER)
    print(
        "The map starts in the top left (position 0), flows to the right, and then snakes down and back to the left\n\n" +
        "Legend:\n" +
        "'_' = regular tile     | '$' = Payday                 | '<' = Opportunity for Children | '@' = Chance to Change Career\n" +
        "'?' = Education Chance | '!' = Romance Opportunity    |\n " 
        )
    print(board)
    print(f"{curr_player} is currently as position {curr_player.position}")
    print(DIVIDER)
    
    # re-establishes the map
    board[row][location] = old_symbol

def initialize_board() -> None:
    # place action squares
    for event in LIST_OF_EVENTS:
        row = 0
        for location in event.positions:
            # 18 is the last column
            if location > 18:
                row = 1
                # this way we can do negative index of it going back 
                location = ( location - 18 )
                board[row][-location] = event.symbol
            # if supposed to be in the top row
            else:
                board[row][location-1] = event.symbol

# this is the menu for editing players at the start
def display_player_menu():
    # the initial menu will be to edit each player
    print(
        DIVIDER +
        f"{ADD_PLAYER}: To Add Player\n" +
        f"{REMOVE_PLAYER}: To Remove Player\n" +
        f"{EXIT}: To Begin\n" +
        f"{END}: To End" + 
        DIVIDER
        )

# brief title screen
def title_screen() -> None:
    print("\nWelcome to a Game of Life! \n")

# this is the player set up
def players_init(player_list: list[Player]):
    valid = False
    initial_players = []
    while not valid:
        display_player_menu()
        # ask for user input each iteration of the loop
        user_input = input("Choose action: ")
        # if they press add player, append to the list of players
        if user_input == ADD_PLAYER:
            new_player = input("Input new player name: ")
            
            #if the user's name is not blank
            if (new_player.strip()) != "":
                initial_players.append(new_player)
                print(f"\nAdded player {new_player}")
            else:
                print("Not a valid player name, no player was added")
                
        # if they press remove player, remove the player
        elif user_input == REMOVE_PLAYER:
            axed_player = ''
            print('Current players: ')
            print(initial_players, sep = ', ')
            axed_player = input(f"input player to be removed: ").strip()
            if axed_player not in initial_players:
                print(f'{axed_player} not found, try again (names are case sensitive)')
            else:
                initial_players.remove(axed_player)
                print(f"{axed_player} removed")
                
        # if they press exit key, check for confirmation
        elif user_input == EXIT:
            if len(initial_players) != 0:
                print(f"\nAre you sure you want to start with the following players? {', '.join(initial_players)} ")
                print("This cannot be changed once the game has begun.\n")
                confirmation = input(f"Press 1 to confirm, or anything else to continue editing: ")
                # if they press 1, end the while loop
                if confirmation == '1':
                    valid = True
                # if they press anything else, don't do anything
                else:
                    print("Returning to editing")
            else:
                print("Cannot begin without players")
        
        elif user_input == END:
            end_game()

        # handle if an incorrect choice was chosen
        else:
            print("Invalid input\n")
            
        print(DIVIDER)
    
    # append the new player names to the actual player_list
    for players in initial_players:
        player_list.append(Player(players))
    # confirm the end of initialization, and the players in the current game
    
    print ("Starting with players:")
    for each in range(len(player_list)):
        print(player_list[each])
    print(DIVIDER)

# ask for player names, to set up the player_list
def initialization(player_list: list[Player]) -> None:
    title_screen()
    players_init(player_list)

def active_game(player_list: list[Player])-> None:
    #may make this random
    active_player = 0
    all_players_retired = False
    # as long as there is 1 eligible player...
    while not all_players_retired:
        # loop through each player in the list in order
        for active_player in range(len(player_list)):
            remaining_player = False
            # if the given player is not retired...
            if not player_list[active_player].retired:
                remaining_player = True
                print(f"{player_list[active_player]}'s Turn\n")
                action_handler(player_list, active_player)
            # if the player is retired...
            else:
                print(f"{player_list[active_player]} is retired, continuing...\n")
        
        # this could be combined with all_players_retired I think
        if not remaining_player:
            all_players_retired = True
            
    print("All players are retired! Thank you for playing!\n")

def main():
    initialization(player_list)
    initialize_board()
    active_game(player_list)
    

if __name__ == '__main__':
    main()