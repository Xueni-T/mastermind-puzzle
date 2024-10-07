'''
    CS5001
    2023 Fall
    Xueni Tang
    Project: mastermind_game
'''
from Marble import Marble
from Point import Point
import turtle
import random
import time
import datetime

class Leaderboard:
    """
    Class: Leaderboard
            A class to represent the information of the leaderboard
    Attributes: player_name: the name of the player
            boardlist: the list of the leaderboard (score, name)
            leaderboard_file: the name of the file to store the leaderboard
    Functions: load_leaderboard, draw_leaderboard, update_leaderboard
    """
    def __init__(self, player_name=""):
        # Gain the player name
        self.player_name = player_name
        self.boardlist = []
        self.leaderboard_file = "leaderboard.txt"
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.color("blue")
    
    def get_player_name(self, player_name):
        """
        Function: get_player_name: Get the player name
        Parameters: player_name: the name of the player
        Returns: None
        """
        player_name = turtle.textinput("CS5001 Mastermind", "Your Name:")
        return player_name
    
    def load_leaderboard(self, filename="leaderboard_error.gif", 
                         position=(0, 0)):
        """
        Function: load_leaderboard: Load the leaderboard from the file
        Parameters: filename: the name of the leaderboard_error gif
                    position: the position to put the leaderboard_error gif
                    error_type: the type of the error
                    error_message: the message of the error
        Returns: None
        """
        try:
            # Load the leaderboard and add it to the leaderboard list
            with open(self.leaderboard_file, "r") as file:
                lines = file.readlines()
                self.boardlist = [line.strip().split(",") for line in lines]
        except FileNotFoundError:
            # Log the error to the error file
            error_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log = f"{error_time} - Error: Leaderboard file not found \n"
            with open("mastermind_errors.err", "a") as file:
                file.write(error_log)
            # Pop up a window to show the error gif
            screen = turtle.Screen()
            screen.addshape(filename)
            # Create a turtle with the GIF
            error_turtle = turtle.Turtle(filename)
            error_turtle.penup()
            error_turtle.goto(position) 
            time.sleep(2)  # Pause for 2 seconds
            turtle.clearscreen() # Clear the screen    
        turtle.update()  # Force update after loading leaderboard

    def draw_leaderboard(self):
        """
        Function: draw_leaderboard
                    Draw the leaders' information on the leaderboard
        Parameters: None
        Returns: None
        """
        self.pen.up()
        self.pen.pencolor("blue")
        # Write the title
        self.pen.goto(130, 280)
        self.pen.write("Leaders:", align="left", font=("Arial", 20, "bold"))
        # Write the scores and names
        self.pen.goto(130, 250)
        for i in range(len(self.boardlist)):
            self.pen.write(f"{self.boardlist[i][0]}: {self.boardlist[i][1]}",
                            align="left", font=("Arial", 15, "normal"))
            self.pen.goto(130, 250 - (i + 1) * 30)

    def update_leaderboard(self, round):
        """
        Function: update_leaderboard
                Update the leaderboard after the player wins the game
        Parameters: round: the round number when the player wins the game
        Returns: None
        """
        round = round + 1 # The score is the round number plus 1
        self.boardlist.append([round, self.player_name])
        # Sort the leaderboard list by the first element (score)
        self.boardlist = sorted(self.boardlist, key=lambda x: int(x[0]))
        # Update the new score and name to the leaderboard file
        with open(self.leaderboard_file, "w") as file:
            for i in range(len(self.boardlist)):
                file.write(f"{self.boardlist[i][0]},{self.boardlist[i][1]}\n")

class Arrow:
    """
    Class: Arrow
            A class to represent the arrow to indicate the processed line
            of the main marbles
    Attributes: x: the start x coordinate of the arrow
                y: the start y coordinate of the arrow
    Functions: draw_arrow, move_arrow
    """
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.color("black")
        self.pen.pensize(2)
        self.start_point = Point(-310, 290)
        self.x = self.start_point.x
        self.y = self.start_point.y

    def draw_arrow(self):
        """
        Function: draw_arrow
                    Draw the shape of arrow to indicate the processed line
                    of the main marbles
        Parameters: None
        Returns: None
        """
        self.pen.up()
        self.pen.goto(self.x, self.y)
        self.pen.fillcolor("red")
        self.pen.begin_fill()
        self.pen.setheading(0) # Keep the direction of the arrow
        self.pen.right(105)
        self.pen.forward(7)
        self.pen.left(150)
        self.pen.forward(20)
        self.pen.left(120)
        self.pen.forward(20)
        self.pen.left(150)
        self.pen.forward(7)
        self.pen.end_fill()
        self.pen.setheading(0) # Keep the direction for next round

    def move_arrow(self, round):
        """
        Function: move_arrow
                Move the arrow to the next line of the main marbles
        Parameters: round: the number of the current round  
        Returns: None
        """
        self.x = self.start_point.x
        if round <= 9: # Avoid moving out of the line of the main marbles
            # The gap between two lines is same as the main marbles gap
            self.y = self.start_point.y - 48 * round 
            self.pen.clear() # Clear the previous arrow
            self.draw_arrow()

class Game:
    """
    Class: Game
            A class to represent the game
    Functions:
            __init__, for_draw_square, draw_square, draw_main_marble, 
            draw_peg_marble, draw_marble_button, insert_gif, insert_buttons,
            check_game_over, draw_pegs, click_choice, start_new_round,
            click_check, click_xbutton, click_quit, check_answer
    """
    def __init__(self, leaderboard, secret_code=[]): 
        # Leaderboard is for updating the scores(round) to leaderboard
        self.leaderboard = leaderboard
        self.screen = turtle.Screen()
        self.screen.title("CS5001 MasterMind Code Game") 
        # Set the screen size of 650 x 650
        self.screen.screensize(650, 650)
        # Initialize the pen for drawing squares
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        # Initialize the list of secret color code
        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]
        # Randomly choose four colors to be the secret code
        self.secret_code = secret_code
        # Initialize some variables for the game
        self.round = 0
        self.maximum_round = 10
        self.bulls_count = 0
        self.cows_count = 0
        self.game_over = False # Initialize the game over status
        # Initialize the empty list of marbles choice, guess colors
        self.marbles_choice = []
        self.current_guess = []
        # Initialize the list of main marbles for storing the main marbles
        self.main_marbles = []
        # Initialize the arrow
        self.arrow = Arrow()
        self.arrow.draw_arrow()

    def generate_secret_code(self, secret_code=[]):
        """
        Function: generate_secret_code: Generate the secret code
        Parameters: None
        Returns: None
        """
        # Randomly choose four colors to be the secret code
        secret_code = random.sample(self.colors, 4)
        return secret_code

    def for_draw_square(self, start_point, width, height, color):
        """
        Function: for_draw_square: Basic function to draw the squares
        Parameters: start_point: the start point of the square
                    width: the width of the square
                    height: the height of the square
                    color: the pen color of the square
        Returns: None
        """
        self.pen.pensize(5)
        self.pen.speed(0)
        self.pen.up()
        self.pen.pencolor(color)  # Set the pen color
        self.pen.goto(start_point.x, start_point.y)
        self.pen.down()
        for _ in range(2):
            self.pen.forward(width)
            self.pen.right(90)
            self.pen.forward(height)
            self.pen.right(90)
        self.pen.up()
    
    def draw_square(self):
        """
        Function: draw_square: Draw the three squares of the game board
        Parameters: None
        Returns: None
        """
        self.for_draw_square(Point(-330, 330), 400, 500, "black")
        self.for_draw_square(Point(105, 330), 225, 500, "blue")
        self.for_draw_square(Point(-330, -200), 660, 100, "black")

    def draw_main_marble(self):
        """
        Function: draw_main_marble
                Draw the empty main marbles and store them in the list
        Parameters: None
        Returns: None
        """
        start_x = -260
        start_y = 280
        gap = 40
        color = 'white'
        # Draw a 10 x 4 matrix of empty main marbles
        for i in range(10):
            main_marbles_four = [] # The list of a line of four marbles
            for j in range(4):
                position = Point(start_x + j * gap, start_y - i * gap * 1.2)
                marble = Marble(position, color, size = 15)
                marble.draw_empty()
                main_marbles_four.append(marble)
            # Store the main marbles for future painting the colors
            self.main_marbles.append(main_marbles_four)
  
    def draw_peg_marble(self): 
        """
        Function: draw_peg_marble: Draw the empty peg marbles
        Parameters: None
        Returns: None
        """       
        start_x = -200
        start_y = 290
        color = ''
        gap = 40
        peg_gap = 15  # Gap between pegs 
        peg_radius = 5  # Radius of pegs
        # Draw a 10 x 2 x 2 matrix of empty peg marbles
        for i in range(10):
            for k in range(2):
                    for l in range(2):
                        small_position = Point(start_x + 4 * gap + peg_gap * 
                                               (k - 0.5), start_y - i * gap * 
                                               1.2 + peg_gap * (l - 0.5))
                        small_marble = Marble(small_position, color, 
                                              size = peg_radius)
                        small_marble.draw_empty() 

    def draw_marble_button(self):
        """ 
        Function: draw_marble_button: Draw the marble buttons with six colors
        Parameters: None
        Returns: None    
        """
        start_x = -290
        start_y = -265
        gap = 40
        for i in range(len(self.colors)):
            marble_color = self.colors[i]
            position = Point(start_x + i * gap, start_y)
            marble_button = Marble(position, marble_color, size = 15)
            marble_button.draw()
            # Add the marble buttons to the list for future reloading
            self.marbles_choice.append(marble_button)

    def insert_gif(self, filename, position=(0, 0)):
        """
        Function: insert_gif:Basic function to insert the GIF
        Parameters: filename: the name of the GIF
                    position: the position to put the GIF
        Returns: None
        """
        try:
            screen = turtle.Screen()
            screen.addshape(filename)
            # Create a turtle with the GIF
            gif_turtle = turtle.Turtle(filename)
            gif_turtle.penup()
            gif_turtle.goto(position)  # Adjust position as needed
        except FileNotFoundError:
            # Pop up a window to show the error gif and exit the game
            self.insert_gif("file_error.gif", 0, 0)
            time.sleep(2)
            turtle.done()     

    def insert_buttons(self):
        """
        Function: insert_buttons
                Insert the buttons of check, xbutton and quit
        Parameters: None
        Returns: None
        """
        self.insert_gif("xbutton.gif", (70, -250))
        self.insert_gif("quit.gif", (250, -250))
        self.insert_gif("checkbutton.gif", (0, -250))
        
    def check_game_over(self):
        """
        Function: check_game_over: Check if the game is over
        Parameters: None
        Returns: True if the game is over, False if not
        """
        if self.round >= self.maximum_round: # Check if the player loses
            self.game_over = True
            # Handle game lose, show lose GIF and exit the game
            self.insert_gif("Lose.gif", (0, 0))
            turtle.update()
            turtle.done()
            return True
        return False
    
    def draw_pegs(self, round):
        """
        Function: draw_pegs: Draw the pegs of the current round
        Parameters: round: the number of the current round
        Returns: None
        """
        cows = self.cows_count
        bulls = self.bulls_count
        logic_answer = self.current_guess
        secret_code = self.secret_code
        pegs_position = [(-46.5, 297.5 - 48 * round), 
                                   (-31.5, 297.5 - 48 * round), 
                                   (-46.5, 282.5 - 48 * round), 
                                   (-31.5, 282.5 -48 * round)]
        if self.check_game_over(): # Check if the game is over
                return
        if logic_answer != secret_code: # Check if the player wins
            if self.round <= self.maximum_round: # Check if the game is over
                i = 0
                # Draw the black pegs of the current round
                if bulls > 0:
                    for i in range(bulls):
                        position = (Point(pegs_position[i][0], 
                                          pegs_position[i][1]))
                        pegs_marble = Marble(position, "black", size = 5)
                        pegs_marble.draw()
                else:
                    pass
                j = 0
                # Draw the red pegs of the current round
                if cows > 0:
                    for j in range(cows):
                        position = (Point(pegs_position[bulls+j][0],
                                            pegs_position[bulls+j][1]))
                        pegs_marble = Marble(position, "red", size = 5)
                        pegs_marble.draw()
                else:
                    pass

    def click_choice(self, x, y):
        """
        Function: click_choice: Handle the mouse click on the marble buttons
        Parameters: x: the x coordinate of the mouse click
                    y: the y coordinate of the mouse click
        Returns: None
        """
        self.x = x
        self.y = y
        # Check if the mouse click is in the areas of the marble buttons
        for i, marble_button in enumerate(self.marbles_choice):
            distance = ((self.x - marble_button.position.x) ** 2 + 
                        (self.y - marble_button.position.y) ** 2) ** 0.5
            if distance <= 15:
                chosen_color = self.colors[i] # Get the chosen color
                # Check if the chosen color is in the current guess            
                if chosen_color not in self.current_guess and \
                        len(self.current_guess) < 4:
                    marble_button.draw_empty() # Clear the marble button
                    # Add the color to the current guess
                    self.current_guess.append(chosen_color)
                    # Show the color on the main marble
                    main_marble = self.main_marbles[self.round]\
                            [len(self.current_guess) - 1]
                    main_marble.set_color(chosen_color)
                    main_marble.draw()
                # Check if four marbles have been chosen
                if len(self.current_guess) == 4:
                    return  # Stop processing clicks  

    def start_new_round(self):
        """
        Function: start_new_round: Start a new round of the game
        Parameters: None
        Returns: None
        """
        # Clear the current guess
        self.current_guess = []
        # Reload the choice marbles for the next round
        for marble_button in self.marbles_choice:
            marble_button.draw()           
        # Update the round number
        self.round += 1
        # Reset cows and bulls count
        self.cows_count = 0
        self.bulls_count = 0
        self.arrow.move_arrow(self.round)  # Move the arrow to the next line                                                    
        # Check for game over
        if self.check_game_over():
            return

    def click_check(self, x, y):
        """
        Function: click_check: Handle the mouse click on the check button
        Parameters: x: the x coordinate of the mouse click
                    y: the y coordinate of the mouse click
        Returns: None
        """
        self.x = x
        self.y = y
        if len(self.current_guess) < 4:
            return  # Ignore clicks if the current guess is not full
        # Check if the mouse click is in the area of the check button
        check_button = {"position": (0, -250)}
        distance = ((self.x - check_button["position"][0]) ** 2 + 
                    (self.y - check_button["position"][1]) ** 2) ** 0.5
        if distance <= 30: # 30 is the radius of the check button
            self.check_answer(self.round) # Pass the round number to check
            self.start_new_round() # Start a new round

    def click_xbutton(self, x, y):
        """
        Function: click_xbutton: Handle the mouse click on the xbutton
        Parameters: x: the x coordinate of the mouse click
                    y: the y coordinate of the mouse click
        Returns: None
        """
        self.x = x
        self.y = y
        # Check if the mouse click is in the area of the xbutton
        xbutton = {"position": (70, -250)}
        distance = ((x - xbutton["position"][0]) ** 2 + 
                    (y - xbutton["position"][1]) ** 2) ** 0.5
        if distance <= 30:  # 30 is the radius of the xbutton
            # Clear the current painted main marbles
            for i in range(len(self.current_guess)):
                main_marble = self.main_marbles[self.round][i]
                main_marble.set_color('white')
                main_marble.draw()
            # Reload the choice marbles
            for marble_button in self.marbles_choice:
                marble_button.draw()
            # Clear the current guess
            self.current_guess = []
    
    def click_quit(self, x, y):
        """
        Function: click_quit: Handle the mouse click on the quit button
        Parameters: x: the x coordinate of the mouse click
                    y: the y coordinate of the mouse click
        Returns: None
        """
        self.x = x
        self.y = y
        # Check if the mouse click is in the area of the quit button
        if 152 < self.x < 348 and -305 < self.y < -195:
            # Handle game quit, show quit GIF and exit the game
            self.game_over = True
            self.insert_gif("quitmsg.gif", (0, 0))
            turtle.update()
            turtle.done()
            return
    
    def check_answer(self, round):
        """
        Function: check_answer: Check the answer of the current guess
        Parameters: round: the number of the current round
        Returns: None
        """
        # If color and position are correct, add 1 to bulls count
        # If color is correct but position is wrong, add 1 to cows count
        if self.game_over == False:
            if self.current_guess[0] == self.secret_code[0]:
                self.bulls_count+= 1
            elif self.current_guess[0] in self.secret_code:
                self.cows_count += 1
            if self.current_guess[1] == self.secret_code[1]:
                self.bulls_count += 1
            elif self.current_guess[1] in self.secret_code:
                self.cows_count += 1
            if self.current_guess[2] == self.secret_code[2]:
                self.bulls_count += 1
            elif self.current_guess[2] in self.secret_code:
                self.cows_count += 1
            if self.current_guess[3] == self.secret_code[3]:
                self.bulls_count += 1
            elif self.current_guess[3] in self.secret_code:
                self.cows_count += 1
            print(self.bulls_count, self.cows_count)
            self.draw_pegs(round) # Draw the pegs of the current round
        # Check if the player wins
        if self.bulls_count == 4:
            # If the player wins, update the scores to the leaderboard
            self.game_over = True
            self.leaderboard.update_leaderboard(round)
            # Handle game win, show winner GIF and exit the game
            self.insert_gif("winner.gif", (0, 0))
            turtle.update()
            turtle.done()
            return
                
def handle_click(x, y):
    """
    Function: handle_click: integrate all the functions for mouse clicks
    Parameters: x: the x coordinate of the mouse click
                y: the y coordinate of the mouse click
    Returns: None
    """
    game.click_choice(x, y)
    game.click_check(x, y)
    game.click_xbutton(x, y)
    game.click_quit(x, y) 

def main():
    # Load and write the leaderboard
    leaderboard = Leaderboard()
    leaderboard.player_name = leaderboard.get_player_name("")
    leaderboard.load_leaderboard()
    leaderboard.draw_leaderboard()
    global game #
    game = Game(leaderboard)
    # Turn off screen updates
    turtle.tracer(0)
    # Draw the board
    game.draw_square()
    game.draw_main_marble()
    game.draw_peg_marble()
    game.draw_marble_button()
    game.insert_buttons()
    game.secret_code = game.generate_secret_code([])
    print(game.secret_code)
    # Turn on the mouse click for the functions in handle_click
    turtle.onscreenclick(handle_click)
    # Turn on screen updates
    turtle.update()
    turtle.done()   
if __name__ == "__main__":
    main()