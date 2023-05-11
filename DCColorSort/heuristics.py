def no_heuristic(state):
    '''
        This function uses no computation at all and just returns 0 (Dijkstra's algorithm)

        Returns:
            (int) : a zero.
    '''
    return 0

def wagdy_heuristic(state):
    '''
        For each succesive pair of balls that are not the same color, add an estimated cost of 2

        Returns:
            f (int) : the heuristic's value.
    '''

def repeated_color_heuristic(state):
    '''
        For each ball that is not the same color of the most repeated color in a tube, add an estimated cost of 1.

        Returns:
            f (int) : the heuristic's value.
    '''
