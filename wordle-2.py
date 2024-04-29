

from spellchecker import SpellChecker
import pygame
from pygame.locals import *
import pandas as pd
import sqlite3

connection = sqlite3.connect('players.db') #initializes SQLite database if it doesn't already exist
#cursor = connection.cursor()
#cursor.execute("CREATE TABLE IF NOT EXISTS player (username TEXT, score INTEGER)")
#cursor.execute("INSERT INTO player VALUES('Zach', 3)")
connection.commit()

df = pd.read_csv('5_lettering.csv') #reading csv file containing 5 letter words

def main():
    connection = sqlite3.connect('players.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username, score FROM player ORDER BY score DESC") #orders the players scores in order to find the global high score
    rows = cursor.fetchall()
    cursor.close()
    if rows == []: #if no players have played yet
        best_player = "ANYONE"
        high_score = "NO SCORES"
    else:
        best_player = rows[0][0]
        high_score = rows[0][1]

    import pygame

    pygame.init()


    import pygame.time


    clock = pygame.time.Clock() 

    #Constants for colours and fonts
    WHITE = (255, 255, 255)
    GREEN = (107,169,100)
    YELLOW = (200,180,88)
    BLACK = (0,0,0)
    GRAY = (120,124,126)
    RED = (255, 0, 0)
    PURPLE = (160,32,240)
    ORANGE = (255, 165, 0)
    BORDER = (127, 127, 127)
    base_font = pygame.font.SysFont('helveticaneue', 90)
    popup_font = pygame.font.SysFont('helveticaneue', 40)
    end_font = pygame.font.SysFont('helveticaneue', 30)
    letter_font = pygame.font.SysFont('helveticaneue', 30)
    streak_font = pygame.font.SysFont('helveticaneue', 30)
    user_font = pygame.font.SysFont('helveticaneue', 30)
    FONT = pygame.font.Font(None, 42)
    
    #constants for size of buttons
    button_width = 1200
    button_height = 1000
    button_text = "RESTART"
    button_text_surface = popup_font.render(button_text, False, WHITE)

    button_width2 = 1200
    button_height2 = 1200
    button_text2 = "QUIT"
    button_text_surface2 = popup_font.render(button_text2, False, WHITE)

    #dataset with 5-letter words
    w = df.sample()
    WORD = "".join((w['word'].values[0]).split(",")).upper() #selecting a random 5-letter word and changing it to uppercase

    MSG = ""

    SQUARE_LENGTH = 100

    colored = [[BLACK for j in range(5)] for i in range(6)] #creating the wordle squares that contain the letters

    spell = SpellChecker(language='en') #initializing English spellchecker

    def is_english_word(word): #function to check if a word is English
        if ",".join(list(word.lower())) in df["word"].values:
            return True
        mispelled = spell.unknown([word])
        if len(mispelled) > 0:
            return False
        else:
            return True

    #defining function to draw rectangle with a border
    def drawStyleRect(surface, input_rect, color, border, length):
        pygame.draw.rect(surface, color, input_rect)
        for i in range(4):
            pygame.draw.rect(surface, border, (input_rect.x-i,input_rect.y-i,length,length), 1, 2, 2, 2, 2, 2)


    pygame.init()

    #initializing user tries, currents words and the alphabet
    tries = 0

    current_list = [["", "", "", "", ""] for i in range(6)] #list of spots containing words typed by user


    alphabet = [["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"], 
                ["N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]]
    
    alpha_box = 50

    alpha_colour = [[BLACK for i in range(13)] for j in range(2)]

    #initializing user's current streak
    streak = 0
    win = False


    gameOn = True
    i = 0
    enter_pressed = -1

    #setting login screen
    screen1 = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Login")
    clock = pygame.time.Clock()
    password = ''

    done = False

    #getting username from user
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    print(password)  # I just print it to see if it works.
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:  # Add the character to the password string.
                    password += event.unicode

        screen1.fill((30, 30, 30))
        # Render the asterisks and blit them.
        password_surface = FONT.render("Enter Username: {}".format(password), True, GREEN) #allows user to sign in
        screen1.blit(password_surface, (30, 30))

        pygame.display.flip()
        clock.tick(30)

    username = password

    screen = pygame.display.set_mode((1100, 1200)) #setting game screen
    pygame.display.set_caption('Wordle Practice')

    connection = sqlite3.connect('players.db')
    cursor = connection.cursor()
    cursor.execute("SELECT username, score FROM player WHERE username = '{}' ORDER BY score DESC".format(username)) #finds user's best score from database 
    player = cursor.fetchall()
    cursor.close()

    if len(player) > 0:
        personal_best = player[0][1]
        registered = True
    else:
        personal_best = 0
        registered = False #determines if player has played before




    screen.fill(BLACK)

    while gameOn: #running game
        for event in pygame.event.get():
            user_surface = user_font.render("SIGNED IN AS: {}".format(username.upper()), False, WHITE) #renders text saying current username
            screen.blit(user_surface, (645, 300))
            streak_surface = streak_font.render("Current Streak: {}".format(streak).upper(), False, GREEN) #renders text saying the streak of the player
            screen.blit(streak_surface, (645, 250))
            if streak > personal_best:
                streak_surface = streak_font.render("Personal Best: {}".format(personal_best).upper(), False, BLACK) #renders text saying the players best score
                screen.blit(streak_surface, (645, 350))
                personal_best = streak
            if streak > high_score:
                streak_surface = streak_font.render("highscore: {0} By {1}".format(high_score, best_player).upper(), False, BLACK) #renders text saying global highscore and by which player
                screen.blit(streak_surface, (645, 400))
                high_score = streak
                best_player = username
            streak_surface = streak_font.render("Personal Best: {}".format(personal_best).upper(), False, PURPLE)
            screen.blit(streak_surface, (645, 350))
            streak_surface = streak_font.render("highscore: {0} By {1}".format(high_score, best_player).upper(), False, ORANGE)
            screen.blit(streak_surface, (645, 400))

            pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN: #checks if mouse button is clicked
                mouse = pygame.mouse.get_pos()
                if button_width/2 <= mouse[0] <= button_width/2+200 and button_height/2 <= mouse[1] <= button_height/2+50: #checks if RESTART button was clicked
                    text_surface2 = end_font.render("THE WORD WAS {}".format(WORD), False, BLACK) #tells user what the word was
                    screen.blit(text_surface2, (630, 150))
                    w = df.sample()
                    WORD = "".join((w['word'].values[0]).split(",")).upper() #picks a new 5-letter word
                    for r in range(len(current_list)):
                        for c in range(len(current_list[r])):
                            current_list[r][c] = ""
                    tries = 0
                    i = 0
                    colored = [[BLACK for j in range(5)] for i in range(6)]
                    alpha_colour = [[BLACK for i in range(13)] for j in range(2)]
                    text_surface = popup_font.render(MSG, False, BLACK)
                    screen.blit(text_surface, (650, 100)) #resets screen
                    streak_surface = streak_font.render("Current Streak: {}".format(streak).upper(), False, BLACK) 
                    screen.blit(streak_surface, (645, 250))
                    if win:
                        streak += 1
                    else:
                        streak = 0
                    win = False
                    streak_surface = streak_font.render("Current Streak: {}".format(streak).upper(), False, GREEN) #current streak increases by 1 if user got word and sets to 0 otherwise
                    screen.blit(streak_surface, (645, 250))

                elif button_width2/2 <= mouse[0] <= button_width2/2+200 and button_height2/2 <= mouse[1] <= button_height2/2+50: #checks if user clicks on QUIT button
                    connection = sqlite3.connect('players.db')
                    cursor = connection.cursor()
                    if registered:
                        cursor.execute("UPDATE player SET score = {0} WHERE username = '{1}'".format(personal_best, username)) #updates players personal best in SQLite database
                    else:
                        cursor.execute("INSERT INTO player VALUES('{0}', {1})".format(username, personal_best)) #updates players personal best in SQLite database
                        #cursor.execute("INSERT INTO player SET score = {0} WHERE username = '{1}'".format(personal_best, username))
                    connection.commit()
                    pygame.quit()

            elif event.type == QUIT: #checks if player quits
                connection = sqlite3.connect('players.db')
                cursor = connection.cursor()
                if registered:
                    cursor.execute("UPDATE player SET score = {0} WHERE username = '{1}'".format(personal_best, username)) #updates players personal best in SQLite database
                else:
                    cursor.execute("INSERT INTO player VALUES('{0}', {1})".format(username, personal_best)) #updates players personal best in SQLite database
                        #cursor.execute("INSERT INTO player SET score = {0} WHERE username = '{1}'".format(personal_best, username))
                connection.commit()
                gameOn = False #game will end
            elif event.type == KEYDOWN: #checks if user presses key
                if event.key == K_BACKSPACE:
                    if i > 0:
                        current_list[tries][i - 1] = current_list[tries][i - 1][:-1]  # Removes last character
                        i -= 1
                elif event.key == K_RETURN: #checks if user presses return
                    user_word = ("").join(current_list[tries]).upper() #creates the user word
                    if len(user_word) < 5: #checks if user word is 5 characters
                        text_surface = popup_font.render(MSG, False, BLACK)
                        screen.blit(text_surface, (650, 100))
                        text_surface = popup_font.render('TOO SHORT', False, YELLOW) #tells user that their word is too short
                        screen.blit(text_surface, (650, 100))
                        MSG = 'TOO SHORT'
                        enter_pressed = -1
                    elif is_english_word(user_word): #checks if user word is English
                        text_surface = popup_font.render(MSG, False, BLACK)
                        screen.blit(text_surface, (650, 100))
                        tries += 1
                        enter_pressed = tries-1
                        for j in range(len(current_list[tries-1])):
                            if current_list[tries-1][j] == WORD[j]:
                                colored[tries-1][j] = GREEN
                                if current_list[tries-1][j] in alphabet[0]:
                                    alpha_colour[0][alphabet[0].index(current_list[tries-1][j])] = GREEN #changes letters to the colour they should be for wordle
                                else:
                                    alpha_colour[1][alphabet[1].index(current_list[tries-1][j])] = GREEN #changes letters to the colour they should be for wordle
                            elif current_list[tries-1][j] in WORD:
                                colored[tries-1][j] = YELLOW
                                if current_list[tries-1][j] in alphabet[0]:
                                    if alpha_colour[0][alphabet[0].index(current_list[tries-1][j])] != GREEN:
                                        alpha_colour[0][alphabet[0].index(current_list[tries-1][j])] = YELLOW #changes letters to the colour they should be for wordle
                                else:
                                    if alpha_colour[1][alphabet[1].index(current_list[tries-1][j])] != GREEN:
                                        alpha_colour[1][alphabet[1].index(current_list[tries-1][j])] = YELLOW #changes letters to the colour they should be for wordle
                            else:
                                colored[tries-1][j] = GRAY
                                if current_list[tries-1][j] in alphabet[0]:
                                    if YELLOW != alpha_colour[0][alphabet[0].index(current_list[tries-1][j])] != GREEN:
                                        alpha_colour[0][alphabet[0].index(current_list[tries-1][j])] = GRAY #changes letters to the colour they should be for wordle
                                else:
                                    if YELLOW != alpha_colour[1][alphabet[1].index(current_list[tries-1][j])] != GREEN:
                                        alpha_colour[1][alphabet[1].index(current_list[tries-1][j])] = GRAY #changes letters to the colour they should be for wordle
                        if user_word == WORD: #checks if user guessed the correct word
                            text_surface = popup_font.render(MSG, False, BLACK)
                            screen.blit(text_surface, (650, 100))
                            text_surface = popup_font.render('YOU WIN', False, GREEN) #tells user they won
                            screen.blit(text_surface, (650, 100))
                            MSG = "YOU WIN"
                            win = True
                        elif tries >= len(current_list): #checks if user has used up all their attempts
                            text_surface = popup_font.render(MSG, False, BLACK)
                            screen.blit(text_surface, (650, 100))
                            text_surface = popup_font.render('YOU LOSE', False, RED)
                            text_surface2 = end_font.render("THE WORD WAS {}".format(WORD), False, RED)
                            screen.blit(text_surface, (650, 100))
                            screen.blit(text_surface2, (630, 150))
                            MSG = "YOU LOSE"
                        else:
                            i = 0 #othrwise text moves to next line
                    else: #if user word is not English
                        enter_pressed = -1
                        text_surface = popup_font.render(MSG, False, BLACK)
                        screen.blit(text_surface, (650, 100))
                        text_surface = popup_font.render('NOT ENGLISH', False, YELLOW)
                        screen.blit(text_surface, (650, 100))
                        MSG = 'NOT ENGLISH'
                elif i <= 4 and event.unicode.isalpha():
                    enter_pressed = -1
                    current_list[tries][i] += event.unicode.upper() #allows user to type to screen
                    i += 1
        mouse = pygame.mouse.get_pos()

        if button_width/2+40 <= mouse[0] <= button_width/2+200 and button_height/2 <= mouse[1] <= button_height/2+50: 
            pygame.draw.rect(screen,GREEN,[button_width/2 + 40,button_height/2,190,50], 2, 3) #changes colour of RESTART box
          
        else: 
            pygame.draw.rect(screen,YELLOW,[button_width/2+40,button_height/2,190,50], 2, 3)

        if button_width2/2+40 <= mouse[0] <= button_width2/2+200 and button_height2/2 <= mouse[1] <= button_height2/2+50: 
            pygame.draw.rect(screen,PURPLE,[button_width2/2 + 40,button_height2/2,190,50], 2, 3) #changes colour of QUIT box
          
        else: 
            pygame.draw.rect(screen,RED,[button_width2/2+40,button_height2/2,190,50], 2, 3)

        screen.blit(button_text_surface,(button_width/2+50,button_height/2))
        screen.blit(button_text_surface2,(button_width2/2+84,button_height2/2))

        for row in range(len(alphabet)): #draws boxes for all letters of the alphabet which show which letters have been used
            for col in range(13):
                input_rect = pygame.Rect(20 + alpha_box*col*1.5, 750 + alpha_box*row*1.5, alpha_box, alpha_box)
                drawStyleRect(screen, input_rect, alpha_colour[row][col], BORDER if alpha_colour[row][col] == BLACK else alpha_colour[row][col], alpha_box)
                letter_surface = letter_font.render(alphabet[row][col], False, WHITE)
                text_width, text_height = letter_font.size(alphabet[row][col])
                screen.blit(letter_surface, (input_rect.centerx-text_width//2, input_rect.centery-text_height//2))
        
        for row in range(len(current_list)): #draws boxes for all word attempts containing text from user
            for col in range(5):
                input_rect = pygame.Rect(20 + SQUARE_LENGTH*col*1.2, 20 + SQUARE_LENGTH*row*1.2, SQUARE_LENGTH, SQUARE_LENGTH)
                drawStyleRect(screen, input_rect, colored[row][col], BORDER if colored[row][col] == BLACK else colored[row][col], SQUARE_LENGTH)
                text_surface = base_font.render(current_list[row][col], True, WHITE)
                text_width, text_height = base_font.size(current_list[row][col])
                screen.blit(text_surface, (input_rect.centerx-text_width//2, input_rect.centery-text_height//2))
                if enter_pressed == row and col < 3:
                    pygame.time.delay(70)
                    pygame.display.flip()
        
        clock.tick(60)

        pygame.display.flip()

main()


