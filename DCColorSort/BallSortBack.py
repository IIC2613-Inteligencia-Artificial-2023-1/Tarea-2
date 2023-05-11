import pygame
import random
import BallSortFront
from BallSortFront import WIDTH, HEIGHT

class BallSortGame:

    '''
        This class controls the flow of the game and can provide available moves to the Solver.
    '''

    def __init__(self, display = False):

        '''
            Parameters:
                display (bool) : whether to or not to display the game.
        '''

        self.init_state = State(False, [], 4)
        self.current_state = self.init_state
        self.display = display

        # Default values for number of tubes and capacity, will be rewritten in self.load_map()
        self.n_tubes = 0
        self.capacity = 4
        if self.display:
            self.start_visualization()

    def load_map(self, map_info):

        '''
            Parameters:
                color (int) : integer representing to the balls color.
        '''

        self.n_tubes = map_info["num_tubes"]
        self.layout = map_info["tubes_layout"]
        self.capacity = map_info["tube_capacity"]

        self.init_state = State(False, self.layout, self.capacity)
        self.current_state = self.init_state

    def move_balls(self, from_idx, to_idx):

        '''
            Emulates the movement of pouring one tube into another without updating the current game's state.

            Parameters:
                from_idx (int) : index of the tube from where the movement is performed.
                to_idx (int) : index of the tube to where the movement is performed.

            Returns:
                new_state (State) : the new state obtained after pouring from on tube into another.
        '''

        if len(self.current_state.tubes[to_idx]) == self.capacity:
            print(f"ERROR: El tubo {to_idx} se encuentra lleno")
            return self.current_state
    
        # Copy the tubes and perform the movement in them
        tubes = [x.copy() for x in self.current_state.tubes.copy()]
        tubes[to_idx].append(tubes[from_idx].pop())

        new_state = State(self.current_state, tubes, self.capacity)
        return new_state

    def get_valid_moves(self):

        '''
            Computes all the valid moves from the current state.

            Returns:
                pairs (list(list(State, list(int, int), int))) :  a list of valid moves in the following format: [new_state, [from_idx, to_idx], cost].
        '''

        pairs = []
        # Loop over the "from" tubes
        for i in range(len(self.current_state.tubes)):
            first_tube = self.current_state.tubes[i]
            # Empty tubes cannot pour balls on other tubes
            if len(first_tube) == 0: continue
            # Tubes with one ball to go will not be used
            if len(first_tube) >= self.capacity - 1 and all(x == first_tube[0] for x in first_tube): continue

            # Loop over the "to" tubes
            for j in range(len(self.current_state.tubes)):
                second_tube = self.current_state.tubes[j]
                # A tube cannot be poured onto himself
                if i == j: continue
                # Balls cannot be poured on full tubes
                if len(second_tube) == self.capacity: continue

                # Otherwise, the movement is valid
                new_state = self.move_balls(i, j)
                pairs.append([new_state, [i, j], 1])

        return pairs

    def start_visualization(self, text = None):

        '''
            Parameters:
                text (str) : optional, text to be displayed at the begining of the visualization.
        '''

        self.display = True
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BallSort")
        self.front = BallSortFront.BallSortGameFront(self.window, self.n_tubes, self.capacity)
        self.front.draw(self.current_state, text = text if text is not None else None)

    def make_move(self, from_idx, to_idx, moving_speed = 12):

        '''
            Performs the movement and updates the current state.

            Parameters:
                from_idx (int) : index of the tube from where the movement is performed.
                to_idx (int) : index of the tube to where the movement is performed.
                moving_speed (int) : speed at which the balls move between tubes (in pixels/frame).
        '''
        
        if self.display:
            self.front.draw_move(self.current_state, from_idx, to_idx, moving_speed)
        self.current_state = self.move_balls(from_idx = from_idx, to_idx = to_idx)
        if self.display:
            self.front.draw(self.current_state)

class State:

    '''
        This class models each state of the Game.
    '''

    def __init__(self, parent, layout, tube_capacity):

        '''
            Parameters:
                parent (State) : previous State of the game.
                layout (list(list(int))) : current layout of the game in the same format as "tubes_layout" on the map's JSON.
                tube_capacity (int) : ammount of balls that you can fit inside of each tube.
        '''

        self.is_init = True if parent == False else False
        self.from_state = parent
        self.tubes = layout
        self.tube_capacity = tube_capacity

    def is_final(self):

        '''
            Computes if current state is final or no.

            Returns:
                (bool) : indicates whether the current stat is or not final.
        '''

        for tube in self.to_list():
            if len(tube) == self.tube_capacity and all(x == tube[0] for x in tube):
                continue
            elif len(tube) == 0:
                continue
            else:
                return False
        return True
    
    def to_list(self):

        '''
            Returns:
                (list(list(int))) :  list containing each one of the tubes and their respective balls.
        '''

        return [tube for tube in self.tubes]
    
    def __str__(self):

        '''
            Returns:
                (str) : string representation of the current state.
        '''

        return str(self.to_list())
    
    def __repr__(self):

        '''
            Returns:
                (str) : object representation of the current state.
        '''

        return str(self.to_list())


if __name__ == "__main__":

    # We create a random sample game
    game = BallSortGame()
    map_data = {"num_tubes": 3, "tube_capacity": 4, "tubes_layout": [[0, 1, 0], [0, 1], [0, 1, 1]]}
    game.load_map(map_data)
    game.start_visualization()

    # Play random moves until the game is won
    while not game.current_state.is_final():
        move = random.choice(game.get_valid_moves())[1]
        game.make_move(move[0], move[1])
    pygame.quit()