import pygame
import os
import json
import matplotlib as plt
if __name__ == "__main__":
    from BallSortBack import BallSortGame

# Intialize PyGame
pygame.init()

ID_FONT = pygame.font.SysFont("comicsans", 20)
WIDTH, HEIGHT = 700, 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TUBE_WIDTH = 40
TUBE_HEIGHT = 150

class TubeFront:

    '''
        This class is in charge of the visual representation of the containers inside of the game.
    '''
    COLOR = WHITE

    def __init__(self, x, y, capacity):

        '''
            Parameters:
                x (int) : position of the tube on the x axis.
                y (int) : position of the tube on the y axis (y = 0 is on the top, y = HEIGHT is on the bottom).
                capacity (int) : ammount of balls that you can fit inside of the tube.
        '''

        self.ball_spacing = 5
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.theta = 0
        self.width = TUBE_WIDTH
        self.height = TUBE_HEIGHT

        # We compute the ball's radius and the position for the last ball on the tube
        self.ball_radius = min(self.width - self.ball_spacing, (self.height - (2 * capacity) * self.ball_spacing) // capacity) // 2
        self.bottom_ball_y = self.y + self.height//2 - self.ball_spacing - self.ball_radius

    def draw(self, win, balls, cmap, id):

        '''
            Parameters:
                win (pygame.display) : window where the game will be displayed.
                balls (list(int)) : list with the contents of the tube (balls represented by integers).
                cmap (matplotlib.cm) : colormap for the balls, it determines which color scale to use.
                id (int) : id of the tubes, display on their bottom.
                draw_changes (bool) : whether to draw or not to draw the ball that just moved.
        '''

        # First off, we draw the tube
        for i in [-1, 1]:
            pygame.draw.circle(win, self.COLOR, (self.x + i * (self.width//2 + self.ball_spacing//2), self.y - self.height//2 + self.ball_spacing), self.ball_spacing)
        pygame.draw.rect(win, self.COLOR, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        pygame.draw.circle(win, self.COLOR, (self.x, self.y + self.height//2), self.width//2)
        id_text = ID_FONT.render(f"{id}", 1, WHITE)
        win.blit(id_text, (self.x - id_text.get_width()//2, self.y + self.height//2 + self.width//2 + 2 * self.ball_spacing))

        pygame.draw.rect(win, BLACK, (self.x - self.width//2 + self.ball_spacing, self.y - self.height//2 + 2 * self.ball_spacing, self.width - 2 * self.ball_spacing, self.height - 2 * self.ball_spacing))
        pygame.draw.circle(win, BLACK, (self.x, self.y + self.height//2), self.width//2 - self.ball_spacing)

        # Then, we fill it out with the balls
        for i in range(len(balls)):
            ball_color = [x * 255 for x in cmap(balls[i])[:3]]
            pygame.draw.circle(win, ball_color, (self.x, self.bottom_ball_y - (2 * i) * (self.ball_radius + self.ball_spacing) + self.width//2 - self.ball_spacing), self.ball_radius)

class BallSortGameFront:

    '''
        This class is in charge of handling all of the game's visuals.
    '''

    def __init__(self, win, n_tubes, tube_capacity):

        '''
            Parameters:
                win (pygame.display) : window where the game will be displayed.
                n_tubes (int) : number of tubes inside of the game.
                tube_capacity (int) : ammount of balls that you can fit inside of each tube.
        '''

        self.window = win
        self.n_tubes = n_tubes
        self.tubes = []
        self.tube_capacity = tube_capacity

        # We create eacth Tube's object
        self.create_tubes()

        # Switch to 'hsv' if more contrast is desired
        self.color_map = plt.cm.get_cmap('Spectral', n_tubes - 1)

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)

    def create_tubes(self):

        '''
            Creates each one of the Tube objects and stores them under self.tubes
        '''

        # We compute the ammount of tubes on each row of the window
        n_bot_tubes = self.n_tubes//2
        n_top_tubes = self.n_tubes - n_bot_tubes

        self.tubes = []
        for i in range(self.n_tubes):
            # Create the tubes on the top side of the window
            if i < n_top_tubes:
                x_tube = (i + 1) * (WIDTH // (1 + n_top_tubes))
                y_tube = HEIGHT // 4 - 20
                self.tubes.append(TubeFront(x = x_tube, y = y_tube, capacity = self.tube_capacity))
            
            # Create the tubes on the bottom side of the window
            else:
                x_tube = (i - n_top_tubes + 1) * WIDTH // (1 + n_bot_tubes)
                y_tube = 3 * HEIGHT // 4 - 20
                self.tubes.append(TubeFront(x = x_tube, y = y_tube, capacity = self.tube_capacity))

    def draw(self, state, text = None):

        '''
            Updates the screen to portrait the game's current state

            Parameters:
                state (State) : current game state.
                text (str) : optional, text to be displayed on the middle of the window.
        '''
        self.window.fill(BLACK)

        # We draw each tube
        i = 0
        for i in range(len(self.tubes)):
            self.tubes[i].draw(self.window, state.to_list()[i], self.color_map, id = i)
            i += 1

        # In case there is text to be displayed, render it
        if text is not None:
            font_render = ID_FONT.render(f"{text}", 1, WHITE)
            self.window.blit(font_render, (WIDTH//2 - font_render.get_width()//2, HEIGHT//2 - font_render.get_height()//2))

        pygame.display.update()

    def draw_move(self, state, from_idx, to_idx, moving_speed = 12):

        '''
            Play the animation for the current move on the display

            Parameters:
                state (State) : current game state.
                from_idx (str) : index of the tube from where the movement is performed.
                to_idx (str) : index of the tube to where the movement is performed.
                moving_speed (int) : speed at which the balls move between tubes (in pixels/frame).
        '''

        # Relevant information about the ball that is about to get moved
        ball_radius = self.tubes[from_idx].ball_radius
        ball_spacing = self.tubes[from_idx].ball_spacing
        ball_color = [x * 255 for x in  self.color_map(state.to_list()[from_idx][-1])[:3]]
        moving_ball_x = self.tubes[from_idx].x
        moving_ball_y = self.tubes[from_idx].bottom_ball_y - (2 * len(state.to_list()[from_idx])) * (ball_radius + ball_spacing) + self.tubes[from_idx].width//2 - ball_spacing
        
        # Target final positions and inbetween goals
        target_x = self.tubes[to_idx].x
        target_y = self.tubes[to_idx].bottom_ball_y - (2 * len(state.to_list()[to_idx])) * (ball_radius + ball_spacing) + self.tubes[to_idx].width//2 - ball_spacing
        from_tube_top_y = self.tubes[from_idx].y - self.tubes[from_idx].height//2 - ball_spacing - ball_radius
        to_tube_top_y = self.tubes[to_idx].y - self.tubes[from_idx].height//2 - ball_spacing - ball_radius

        ''' Lift the ball '''
        while moving_ball_y > from_tube_top_y:
            self.draw_static(state, from_idx)
            moving_ball_y -= moving_speed
            pygame.draw.circle(self.window, ball_color, (moving_ball_x, moving_ball_y), ball_radius)
            pygame.display.update()
            self.clock.tick(FPS)

        ''' Move the ball towards the top of the other tube ''' 
        # Depending on the lowest distance amongst the axes, we will compute the step_size of the smaller distance
        diff_x = abs(moving_ball_x - target_x)
        diff_y = abs(moving_ball_y - to_tube_top_y)

        step_x = moving_speed
        step_y = moving_speed

        if diff_x >= diff_y:
            step_x = moving_speed
            step_y = (diff_y * moving_speed) / diff_x
        else:
            step_y = moving_speed
            step_x = (diff_x * moving_speed) / diff_y

        # Move the ball and update it's visuals on each frame
        while diff_x > step_x or diff_y > step_y:
            self.draw_static(state, from_idx)
            
            if diff_x > step_x:
                moving_ball_x = moving_ball_x - step_x if moving_ball_x > target_x else moving_ball_x + step_x
            else:
                moving_ball_x = target_x
            
            if diff_y > step_y:
                moving_ball_y = moving_ball_y - step_y if moving_ball_y > to_tube_top_y else moving_ball_y + step_y
            else:
                moving_ball_y = to_tube_top_y

            pygame.draw.circle(self.window, ball_color, (moving_ball_x, moving_ball_y), ball_radius)
            pygame.display.update()
            self.clock.tick(FPS)

            diff_x = abs(moving_ball_x - target_x)
            diff_y = abs(moving_ball_y - to_tube_top_y)

        ''' Place on top of tube '''
        self.draw_static(state, from_idx)
        moving_ball_x = target_x
        moving_ball_y = to_tube_top_y
        pygame.draw.circle(self.window, ball_color, (moving_ball_x, moving_ball_y), ball_radius)
        pygame.display.update()
        self.clock.tick(FPS)

        ''' Drop the ball '''
        while moving_ball_y < target_y:
            self.draw_static(state, from_idx)
            moving_ball_y += moving_speed
            pygame.draw.circle(self.window, ball_color, (moving_ball_x, moving_ball_y), ball_radius)
            pygame.display.update()
            self.clock.tick(FPS)
        
        # Add a little bounce for a better looking animation
        moving_ball_y += moving_speed // 2
        pygame.draw.circle(self.window, ball_color, (moving_ball_x, target_y + moving_speed), ball_radius)
        pygame.display.update()
        self.clock.tick(FPS)

    def draw_static(self, state, from_idx):

        '''
            Updates the screen to portrait the game's current state,
            but only the items that have not moved inbetween the current and previous states

            Parameters:
                state (State) : current game state.
                from_idx (int) : index of the tube that was poured to reach the current state.
        '''

        self.window.fill(BLACK)
        i = 0
        for i in range(len(self.tubes)):
            self.tubes[i].draw(self.window, state.to_list()[i] if i != from_idx else state.to_list()[i][:-1], self.color_map, id = i)
            i += 1


if __name__ == "__main__":

    # Load a game map
    game_map = "map_5"
    relative_map_path = os.path.join("maps", f"{game_map}.json")
    current_path = os.path.dirname(os.path.realpath(__file__))
    map_path = os.path.join(current_path, relative_map_path)
    with open(map_path, 'r') as f:
        map_data = json.load(f)

    # Create a game instance
    game = BallSortGame()
    game.load_map(map_data)
    game.start_visualization()
    
    # Display the layout for a few seconds, useful for debugging
    pygame.time.delay(8000)
    pygame.quit()