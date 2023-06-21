import pygame
import random
import time

level = 1
lines_to_clear = 1

#block colors
colors = [
    #red
    (213, 0, 0),
    #cyan
    (100, 179, 179),
    #navy
    (34, 34, 152),
    #magenta
    (220, 28, 28),
    #purple
    (163, 26, 191),
    #yellow
    (255, 171, 0)
]


#configuring the blocks
class Figure:
    x = 0
    y = 0


    figures = [
        #the numbers are the individual blocks in a 4*4 square, and are used to configure the shapes
        #I shape
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        #Z shape
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        #S shape
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        #J shape
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        #L shape
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        #T shape
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        #O shape
        [[1, 2, 5, 6]],

    ]
    
    #a method of a collection of block and color selection, and block rotation
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #randomly selects shape and color from the previous lists
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    #used to show the rotated version of each shape
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


#the tetris class (where all the vital stuff for the game is)
class Tetris:
    level = 1
    score = 0
    #keeps the score (how many lines were cleared)
    score = 0
    #state of the game
    state = "start"
    #keeps track of the 200 squares
    field = []
    height = 0
    width = 0
    #x and y coordinates where the blocks will start down_slowing from
    x = 100
    y = 60
    #adds color to the squares when the block (or parts of it) are there
    cfill = 20
    figure = None

    #initializes the game
    def __init__(self, height, width):
        #gets the x and y coordinates for where the blocks start
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)


    def create_figure(self):
        self.figure = Figure(3, 0)

    #checks if the moving blocks are touching the pre-existing blocks or the edge of the gamescreen
    def b_contact(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    # if the blocks are touching, "contact" becomes true and returns its values
                    # the grid is filled with zeros, and the blocks (which are numbers) fill them
                    # a 0 means the grid is empty, a number means it is full
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0: # the block could be any number larger than 0
                        intersection = True
        return intersection

    #checks if any of the rows are completed and lowers the incomplete rows
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for x in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[x][j] = self.field[x - 1][j]
        #adds points for every line cleared
        self.score += lines
        #calls check_level_up to check if the next level can be reached
        self.check_level_up()

    #checks if the next level can be reached
    def check_level_up(self):
        if self.score >= self.level:
            self.level += 1
            self.score = 0
            self.figure.y += 1
            return True 

    # if the down arrow is held down, the figure down_slows at a faster speed
    def down_fast(self):
        while not self.b_contact():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # if
    def down_slow(self):
        self.figure.y += 1
        if self.b_contact():
            self.figure.y -= 1
            self.freeze()

    # now that we can see if the blocks are making contact, we need to be able to pin the blocks in position.
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        # calls break_lines
        # then calls create_figure and creates new figure
        self.break_lines()
        self.create_figure()
        #if the figure immediateley contacts the existing blocks, the game state is "gameover"
        if self.b_contact():
            self.state = "gameover"

    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.b_contact():
            self.figure.rotation = previous_rotation

    def go_side(self, dx):
        previous_x = self.figure.x
        self.figure.x += dx
        if self.b_contact():
            self.figure.x = previous_x

    def reset_score(self):
        self.level = 0
        self.score = 0


# Initialize the game engine
pygame.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# setting the screen
size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0
content = []

pressing_down = False

#display start screen image
start_screen = pygame.image.load('tetris_sp.png').convert_alpha()
s_background = start_screen.get_rect(center = (200, 250))
screen.blit(start_screen, s_background)
pygame.display.update()
time.sleep(1)


#the main loop
while not done:

    if game.figure is None:
        game.create_figure()
        time.sleep(0.5)
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.down_slow()

    # assign movement for figures with arrow keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            #up arrow to rotate
            if event.key == pygame.K_UP:
                game.rotate()
            #down arrow to fall
            if event.key == pygame.K_DOWN:
                pressing_down = True
            #left arrow to move left
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            #right arrow to move right
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            #space to slow down
            if event.key == pygame.K_SPACE:
                game.down_slow()
            #ESC to start again once the game is over
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
                game.reset_score()

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(white)

    #drawing the grid
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, gray, [game.x + game.cfill * j, game.y + game.cfill * i, game.cfill, game.cfill], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.cfill * j + 1, game.y + game.cfill * i + 1, game.cfill - 2, game.cfill - 1])

    #displaying the figures
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.cfill * (j + game.figure.x) + 1,
                                      game.y + game.cfill * (i + game.figure.y) + 1,
                                      game.cfill - 2, game.cfill - 2])

    #all the texts
    font = pygame.font.SysFont('Calibri', 15, True, False)
    font1 = pygame.font.SysFont('Calibri', 70, True, False)
    #score
    text = font.render("Score / Lines Cleared: " + str(game.score), True, black)
    #level
    text1 = font.render("Level / Lines to Clear: " + str(game.level), True, black)
    #end texts
    text_game_over = font1.render("Game Over!", True, black)
    text_game_over1 = font1.render("Press ESC", True, black)

    screen.blit(text, [10, 10])
    screen.blit(text1, [10, 30])

    #display end texts when game is over
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 180])
        screen.blit(text_game_over1, [40, 275])
    
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()