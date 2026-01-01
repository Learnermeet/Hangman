#########################################################
## File Name: hangman.py                               ##
## Description: Hangman project                        ##
#########################################################
import pygame
import random
import datetime

pygame.init()
clock = pygame.time.Clock()
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
winWidth, winHeight = win.get_size()


BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('assets/hangman0.jpg'), pygame.image.load('assets/hangman1.jpg'), pygame.image.load('assets/hangman2.jpg'), pygame.image.load('assets/hangman3.jpg'), pygame.image.load('assets/hangman4.jpg'), pygame.image.load('assets/hangman5.jpg'), pygame.image.load('assets/hangman6.jpg')]

quit_font = pygame.font.SysFont("arial", 22)
popup_font = pygame.font.SysFont("arial", 26)

# Quit button properties
QUIT_BTN_W = 140
QUIT_BTN_H = 40
quit_btn_rect = pygame.Rect(
    winWidth - QUIT_BTN_W - 20,
    winHeight - QUIT_BTN_H - 20,
    QUIT_BTN_W,
    QUIT_BTN_H
)

#Popup state
show_confirm = False

#Popup box
POPUP_W = 400
POPUP_H = 200
popup_rect = pygame.Rect(
    winWidth / 2 - POPUP_W / 2,
    winHeight / 2 - POPUP_H / 2,
    POPUP_W,
    POPUP_H
)

yes_btn_rect = pygame.Rect(popup_rect.x + 60, popup_rect.y + POPUP_H - 70, 100, 40)
no_btn_rect = pygame.Rect(popup_rect.x + POPUP_W - 160, popup_rect.y + POPUP_H - 70, 100, 40)

paused = False

limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(GREEN)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1, (winWidth / 2 - length / 2, winHeight - 70))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    # Draw Quit Button
    pygame.draw.rect(win, RED, quit_btn_rect, border_radius=8)
    quit_text = quit_font.render("QUIT GAME", True, WHITE)
    win.blit(
        quit_text,
        (
            quit_btn_rect.centerx - quit_text.get_width() / 2,
            quit_btn_rect.centery - quit_text.get_height() / 2
        )
    )


def draw_confirm_popup():
    # Dark overlay
    overlay = pygame.Surface((winWidth, winHeight))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))

    # Popup box
    pygame.draw.rect(win, WHITE, popup_rect, border_radius=10)
    pygame.draw.rect(win, BLACK, popup_rect, 2, border_radius=10)

    # Text
    text = popup_font.render("Are you sure you want to quit?", True, BLACK)
    win.blit(
        text,
        (popup_rect.centerx - text.get_width() / 2,
         popup_rect.y + 40)
    )

    # YES
    pygame.draw.rect(win, GREEN, yes_btn_rect, border_radius=6)
    yes_text = popup_font.render("YES", True, BLACK)
    win.blit(
        yes_text,
        (yes_btn_rect.centerx - yes_text.get_width() / 2,
         yes_btn_rect.centery - yes_text.get_height() / 2)
    )

    # NO
    pygame.draw.rect(win, RED, no_btn_rect, border_radius=6)
    no_text = popup_font.render("NO", True, WHITE)
    win.blit(
        no_text,
        (no_btn_rect.centerx - no_text.get_width() / 2,
         no_btn_rect.centery - no_text.get_height() / 2)
    )

def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    win.fill(GREEN)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The Movie was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
            if event.type == pygame.WINDOWFOCUSGAINED:
                restore_display()
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

def restore_display():
    global win, winWidth, winHeight
    pygame.display.quit()
    pygame.display.init()
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    winWidth, winHeight = win.get_size()
    redraw_game_window()
    pygame.display.flip()



# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = randomWord()
inPlay = True

while inPlay:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
            elif event.key == pygame.K_s:
                filename = "screenshots/hangman_{}.png".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                pygame.image.save(win, filename)
                print("Screenshot saved as {}".format(filename))

        if event.type == pygame.WINDOWFOCUSLOST:
            paused = True

        if event.type == pygame.WINDOWFOCUSGAINED:
            paused = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()

            if show_confirm:
                if yes_btn_rect.collidepoint(clickPos):
                    pygame.quit()
                    quit()
                if no_btn_rect.collidepoint(clickPos):
                    show_confirm = False
                continue

            if quit_btn_rect.collidepoint(clickPos):
                show_confirm = True
                continue
            
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)
    if paused:
        continue
    redraw_game_window()
    if show_confirm:
        draw_confirm_popup()
    pygame.display.flip()

pygame.quit()