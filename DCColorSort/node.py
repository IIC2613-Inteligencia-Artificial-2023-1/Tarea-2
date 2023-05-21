class Node:

    '''
        This class models the nodes used by the solver.
    '''

    def __init__(self, search_state, parent = False, action = []):

        '''
            Parameters:
                search_state (State) : current state of the game.
                parent (Node) : parent node of the current one.
                action (list(int, int)) : list that contains the action performed in order to reach this state (from_idx, to_idx).

        '''

        self.state = search_state
        self.parent = parent
        self.action = action

        # F function for the node
        self.key = -1

        self.g = 10000000000
        self.heap_index = 0
        self.h = -1

    def __repr__(self):

        '''
            Returns:
                (str) : object representation of the current node's state.
        '''

        return self.state.__repr__()
    
    def trace(self):

        '''
            Returns:
                (str), (list(list(int, int))) : string containing the step-by-step solution and each one of the actions inside of it, in order.
        '''

        # If the node does have a parent, ask for the moves that came before it
        if self.parent:
            s, actions = self.parent.trace()
            s += f"\n -{self.action}-> \n"
            s += str(self.state)
            actions = actions + [self.action]

        # If the node has no parent (it's the initial node, return the first action ever perfomed)
        else:
            s = str(self.state)
            actions = []
            
        return s, actions
