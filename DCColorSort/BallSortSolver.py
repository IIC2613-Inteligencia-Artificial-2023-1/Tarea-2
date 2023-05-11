import pygame
import time
import json
import os

import BallSortBack
from binary_heap import BinaryHeap
from node import Node
import heuristics

HEURISTIC_PONDERATOR = 10
VISUALIZATION = False
MOVING_SPEED = 15

# Replace with the map to be tested
GAME_MAP = "map_2"

# Compute the map's absolute path
relative_map_path = os.path.join("maps", f"{GAME_MAP}.json")
current_path = os.path.dirname(os.path.realpath(__file__))
MAP_PATH = os.path.join(current_path, relative_map_path)

# Load the map's data
with open(MAP_PATH, 'r') as f:
    MAP_DATA = json.load(f)

class AStarSolver():

    '''
        This class models the solver for the game and performs the A* algorithm in order to find a solution for it.
    '''

    def __init__(self, heuristic = heuristics.no_heuristic, visualization = VISUALIZATION, map_info = MAP_DATA):

        '''
            Parameters:
                heuristic (function) : function used as heuristic for the search (should take a State as an input and output a number), no heuristic by default.
                visualization (bool) : whether to or not to display the solution after it's found.

        '''

        self.expansions = 0
        self.generated = 0

        # Load the map's data
        self.game = BallSortBack.BallSortGame()
        self.game.load_map(map_info)
        self.initial_state = self.game.init_state

        self.heuristic = heuristic
        self.open = BinaryHeap()

        if visualization:
            self.game.start_visualization(text = "Solving...")

    def search(self):

        '''
            Performs the A* search for a solution.
        '''

        # IMPLEMENTAR
        
if __name__ == "__main__":
    # We create an instance for the solver and perform the search on the current map
    solver = AStarSolver(heuristic = heuristics.same_as_bottom_heuristic, visualization = VISUALIZATION)
    sol = solver.search()

    # In case a solution was found, try it out
    if sol[0] is not None:
        solver.game.current_state = solver.game.init_state
        for step in sol[0][1]:
            solver.game.make_move(step[0], step[1], moving_speed = MOVING_SPEED)

        if VISUALIZATION:
            solver.game.front.draw(solver.game.current_state, text = ":)")
            pygame.time.wait(8000) 
            pygame.quit()

        print("The search was succesful at finding a solution.")
        print(f"The number of expansions: {solver.expansions}")
        print(f"The time it took to find a solution: {solver.end_time - solver.start_time}")
        print(f"Number of steps: {len(sol[0][1])}")