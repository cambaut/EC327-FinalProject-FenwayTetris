import pygame
import random


# sets board, block, and screen sizes
BOARD_WIDTH = 20
BOARD_HEIGHT = 21
BLOCK_SIZE = 45
SIDE_WIDTH = 325

SCREEN_WIDTH = BOARD_WIDTH * BLOCK_SIZE + SIDE_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE

# Fenway/Boston themed colors for the block shapes
COLORS = {
    0: (12, 35, 64),     # Boston navy background
    1: (189, 48, 57),    # Fenway red
    2: (54, 123, 202),   #boston city flag blue
    3: (0, 50, 30),      # Green Monster green
    4: (30, 64, 175),    # Boston blue
    5: (212, 175, 55),   # Gold accent
    6: (34, 139, 34),    # Field green
    7: (120, 120, 120)   # Concrete gray
}

#Creates block shapes 
SHAPES = [
    [[1, 1, 1, 1]],
    [[2, 2], [2, 2]],
    [[0, 3, 0], [3, 3, 3]],
    [[4, 0, 0], [4, 4, 4]],
    [[0, 0, 5], [5, 5, 5]],
    [[6, 6, 0], [0, 6, 6]],
    [[0, 7, 7], [7, 7, 0]]
]


class TetrisEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  #adjusts game to take up the entire screen
        pygame.display.set_caption("Fenway Tetris") 

        self.clock = pygame.time.Clock()

        # sets fonts and images
        self.fontbigger = pygame.font.SysFont("arialblack", 42) #before arialblack
        self.font_medium = pygame.font.SysFont("Jersey10-Regular.ttf", 36, bold=True) 
        self.font_small = pygame.font.SysFont("Jersey10-Regular.ttf", 26) #utilizes uploaded font
        self.font_instructions = pygame.font.Font("Jersey10-Regular.ttf", 30) #utilizes uploaded font for the instructions 
        self.start_image = pygame.image.load("fenwaypark.png").convert_alpha()  #adds image of fenway park
        self.start_image = pygame.transform.scale(self.start_image, (self.screen.get_width() +3, self.screen.get_height()))  #sets fenway image to specific size
        self.sidebar_image = pygame.image.load("redsoxplayer.png").convert_alpha() #red sox player image
        self.sidebar_image = pygame.transform.scale(self.sidebar_image, (250, 200)) #resized red sox player image

        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.paused = False

        self.fall_time = 0
        self.fall_speed = 500
        self.round = 1
        self.lines_in_round = 0 #initial lines cleared in round set to 0
        self.lines_per_round = 3 # each round to increase if 3 lines are cleared

        self.spawnpiece()
        self.run()

    #code to spawn different pieces
    def spawnpiece(self):
        self.piece_shape = random.choice(SHAPES)

        self.piece_color_idx = next(
            val for row in self.piece_shape for val in row if val != 0
        )

        self.piece_x = BOARD_WIDTH // 2 - len(self.piece_shape[0]) // 2
        self.piece_y = 0

        if not self.valid(0, 0):
            self.game_over = True

    def valid(self, dx, dy, shape=None):
        shape = shape or self.piece_shape

        for r, row in enumerate(shape):
            for c, val in enumerate(row):
                if val:
                    nx = self.piece_x + c + dx
                    ny = self.piece_y + r + dy

                    if nx < 0 or nx >= BOARD_WIDTH:
                        return False
                    if ny >= BOARD_HEIGHT:
                        return False
                    if ny >= 0 and self.board[ny][nx]:
                        return False

        return True
    
    #to move blocks
    def move(self, dx, dy):
        if not self.game_over and self.valid(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    #to rotate blocks
    def rotate(self):
        transfshape = [list(row) for row in zip(*self.piece_shape[::-1])]

        if self.valid(0, 0, transfshape):
            self.piece_shape = transfshape

    #to hard drop the blocks
    def harddrop(self):
        while self.valid(0, 1):
            self.piece_y += 1

        self.lockpiece()

    def lockpiece(self):
        for r, row in enumerate(self.piece_shape):
            for c, val in enumerate(row):
                if val:
                    board_x = self.piece_x + c
                    board_y = self.piece_y + r

                    if board_y >= 0:
                        self.board[board_y][board_x] = self.piece_color_idx

        self.clearlines()
        self.spawnpiece()

    #code to clear lines
    def clearlines(self):
        shiftedboard = [row for row in self.board if 0 in row]
        lines_cleared = BOARD_HEIGHT - len(shiftedboard)
        #code for keeping track of how many lines have been cleared
        if lines_cleared > 0:
            self.score += lines_cleared * 100
            self.lines_in_round += lines_cleared
            if self.lines_in_round >= self.lines_per_round:
                self.nextround()

        for _ in range(lines_cleared):
            shiftedboard.insert(0, [0] * BOARD_WIDTH)

        self.board = shiftedboard

    #code to draw blocks
    def drawblock(self, x, y, color):
        rect = pygame.Rect(
            x * BLOCK_SIZE,
            y * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE
        )

        # Main block
        pygame.draw.rect(self.screen, color, rect)

        # ark border, like scoreboard tiles
        pygame.draw.rect(self.screen, (20, 20, 20), rect, 2)

        # Highlight line
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (rect.left + 3, rect.top + 3),
            (rect.right - 3, rect.top + 3),
            1
        )
    #makes blocks fall faster after every round
    def nextround(self):
        self.round += 1
        self.lines_in_round = 0
        self.fall_speed = max(100, self.fall_speed - 50)

    def drawboard(self):
        # Draw blocks already locked on the board
        for r in range(BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                color_idx = self.board[r][c]

                if color_idx:
                    self.drawblock(c, r, COLORS[color_idx])

        # Draw current falling block
        for r, row in enumerate(self.piece_shape):
            for c, val in enumerate(row):
                if val:
                    self.drawblock(
                        self.piece_x + c,
                        self.piece_y + r,
                        COLORS[self.piece_color_idx]
                    )

    #creates the sidebar with instructions, image, and score
    def sidebar(self):
        sidebar_x = BOARD_WIDTH * BLOCK_SIZE

        # Green sidebar
        pygame.draw.rect(
            self.screen,
            (48,170,73),
            (sidebar_x, 0, 585, SCREEN_HEIGHT)   #sets sizing
        )

        title = self.fontbigger.render("TETRIS", True, (255, 0, 13)) #sets Tetris heading on side bar
        self.screen.blit(title, (sidebar_x + 200, 60))

        score_text = self.font_medium.render("SCORE", True, (12, 35, 64)) #sets Score on side bar
        score_number = self.font_medium.render(str(self.score), True, (255, 255, 255))
        

        self.screen.blit(score_text, (sidebar_x + 240, 140)) #positions score text 
        self.screen.blit(score_number, (sidebar_x + 280, 175)) #positions user score

        roundcounter = self.font_medium.render(f"ROUND {self.round}", True, (255, 255, 255)) #keeps track of round to display on sidebar
        self.screen.blit(roundcounter, (sidebar_x + 240, 220))
        

        #instructions for the game are listed, font doesn't take arrows so we had to improvise 
        instructions = [

            "Prevent the blocks from reaching the top of the", 
            "board by clearing rows of blocks!",
            "",
            "Each piece can be moved with the arrow keys!",
            "                 <-  = move left",
            "                 ->  = move right",
            "                 Space  = Hard drop!",
            "                 ^  = rotate piece",
            "",
            "If a row of the same color is cleared, you earn",
            "extra points!",
            "",
            "Press “p” on the keyboard to pause!",
            "",
            "Press “esc” to quit and close screen!"
        ]

        y = 300
        for line in instructions:
            text = self.font_instructions.render(line, True, (255, 255, 255))
            self.screen.blit(text, (sidebar_x + 35, y))
            y += 25

        self.screen.blit(
            self.sidebar_image,
            (sidebar_x + 160, y + 94)
            )
        
    #creates the home screen
    def homescreen(self):
        self.screen.fill((255, 255, 255))

        self.screen.blit(
            self.start_image,
            (0,0) 
        )


        title = self.fontbigger.render("FENWAY TETRIS", True, (255, 255, 255)) #sets fenwaypark title, color is white
        enterstart = self.font_medium.render("PRESS ENTER TO START", True, (255, 255, 255)) #sets to start title, color is white
        inspiration = self.font_small.render("*Inspired by Fenway Park*", True, (255, 255, 255)) #sets fenwaypark inspiration title, color is white
        instructions = self.font_small.render("Use arrow keys to move and rotate", True, (255, 255, 255)) #sets instructions title, color is white

        self.screen.blit(title, (SCREEN_WIDTH // 2 + 450 // 2, 90)) #postions text for "FENWAY TETRIS"
        self.screen.blit(enterstart, (SCREEN_WIDTH // 2 + 540 // 2,190)) #postions text for "PRESS ENTER TO START"
        self.screen.blit(inspiration, (SCREEN_WIDTH // 2  + 640 // 2, 160)) #postions text for "Inspired by .."
        self.screen.blit(instructions, (SCREEN_WIDTH // 2 + 554 // 2, 230)) #postions text for instructions 


        pygame.display.update()

    #creates game over screen when user loses
    def gameover(self):
        overlay = self.fontbigger.render("GAME OVER", True, (189, 48, 57))
        self.screen.blit(overlay, (55, SCREEN_HEIGHT // 2 - 30))

    def draw(self):
        # Main background
        self.screen.fill((255, 255, 255))

        self.drawboard()
        self.sidebar()

        #creates border around board
        pygame.draw.rect(
            self.screen,
            (212, 175, 55),
            (0, 0, BOARD_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT),
            3
        )

        if self.game_over:
            self.gameover()

        if self.paused:
            self.pausedscreen()

        pygame.display.update()
    
    #code for when the game is running
    def run(self):
        running = True

        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN: #for specific keys that are pressed

                    if event.key == pygame.K_ESCAPE: #if esc button pressed, game stops running
                        running = False

                    if event.key == pygame.K_RETURN: #if return entered, game starts 
                        self.game_started = True

                    if event.key == pygame.K_p: #if p pressed, game pauses
                        self.paused = not self.paused

                    elif not self.paused and self.game_started: #if the game is not paused and the game stars, for arrow buttons & space
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:
                            self.harddrop()

            if not self.game_started: #if the game has not started, sets the home screen
                self.homescreen()
                continue

            self.fall_time += dt

            if not self.game_over and not self.paused and self.fall_time >= self.fall_speed:
                if self.valid(0, 1):
                    self.piece_y += 1
                else:
                    self.lockpiece()

                self.fall_time = 0

            self.draw()

        pygame.quit()

    #makes the pause game screen
    def pausedscreen(self):
        overlay = pygame.Surface((1500, 1000)) #dimensions to fill screen with paused screen
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        text = self.fontbigger.render("PAUSED", True, (255,255,255)) #"Paused" text on paused screen
        self.screen.blit(
            text,
            (
                SCREEN_WIDTH // 2 + 110 // 2, 
                SCREEN_HEIGHT // 2 - text.get_height() // 2
            )
        )


if __name__ == "__main__":
    TetrisEngine()

