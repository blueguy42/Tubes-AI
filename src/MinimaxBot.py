from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import numpy as np

class MinimaxBot(Bot):
    def __init__(self, num_of_dots: int):
        self.NUMBER_OF_DOTS = num_of_dots
    # minimax with alpha beta pruning
    # player1 as min, player2 (AI) as max
    def get_action(self, state: GameState) -> GameAction:
        print(state.row_status)
        best_action = None
        best_value = -np.inf
        for action in self.get_actions(state):
            value = self.minimax(self.update_board(state, action), -1, -np.inf, np.inf)
            if value > best_value:
                best_value = value
                best_action = action
        print(best_action)
        return best_action

    def is_terminal(self, state: GameState) -> bool:
        return np.all(state.row_status == 1) and np.all(state.col_status == 1)
    
    def get_utility(self, state: GameState) -> int:
        return np.sum(state.board_status)
    
    # def get_utility(self, state: GameState) -> int:
    #     value = 0
    #     for y in range(state.board_status.shape[0]):
    #         for x in range(state.board_status.shape[1]):
    #             if state.board_status[y][x] == 4:
    #                 value += 1000
    #             elif state.board_status[y][x] == -4:
    #                 value -= 1000
    #             elif state.board_status[y][x] == 3:
    #                 value -= 100
    #             elif state.board_status[y][x] == -3:
    #                 value += 100
    #             elif state.board_status[y][x] == 2:
    #                 value += 10
    #             elif state.board_status[y][x] == -2:
    #                 value -= 10
    #             elif state.board_status[y][x] == 1:
    #                 value -= 1
    #             elif state.board_status[y][x] == -1:
    #                 value += 1
    #     return value
    
    def get_actions(self, state: GameState) -> list:
        [ny, nx] = state.row_status.shape
        actions = []
        for y in range(ny):
            for x in range(nx):
                if state.row_status[y][x] == 0:
                    actions.append(GameAction('row', (x, y)))

        [ny, nx] = state.col_status.shape
        for y in range(ny):
            for x in range(nx):
                if state.col_status[y][x] == 0:
                    actions.append(GameAction('col', (x, y)))
        return actions

    def update_board(self, state: GameState, action: GameAction) -> GameState:
        # Taken from main.py with modifications
        new_board_status = state.board_status.copy()
        new_row_status = state.row_status.copy()
        new_col_status = state.col_status.copy()
        new_player1_turn = not state.player1_turn

        action_type = action.action_type
        logical_position = action.position
        x = logical_position[0]
        y = logical_position[1]
        val = 1
        playerModifier = 1
        if state.player1_turn:
            playerModifier = -1
            

        if y < (self.NUMBER_OF_DOTS -1) and x < (self.NUMBER_OF_DOTS-1):
            new_board_status[y][x] = (abs(new_board_status[y][x]) + val) * playerModifier
            if abs(new_board_status[y-1][x]) == 4:
                new_player1_turn = not state.player1_turn

        if action_type == 'row':
            new_row_status[y][x] = 1
            if y >= 1:
                new_board_status[y-1][x] = (abs(new_board_status[y-1][x]) + val) * playerModifier
                if abs(new_board_status[y-1][x]) == 4:
                    new_player1_turn = not state.player1_turn

        elif action_type == 'col':
            new_col_status[y][x] = 1
            if x >= 1:
                new_board_status[y][x-1] = (abs(new_board_status[y][x-1]) + val) * playerModifier
                if abs(new_board_status[y][x-1]) == 4:
                    new_player1_turn = not state.player1_turn

        return GameState(new_board_status, new_row_status, new_col_status, new_player1_turn)

    def minimax(self, state: GameState, depth: int, alpha: int, beta: int) -> int:
        if self.is_terminal(state) or depth == 3:
            return self.get_utility(state)
        if state.player1_turn:
            return self.min_value(state, depth, alpha, beta)
        else:
            return self.max_value(state, depth, alpha, beta)

    def max_value(self, state: GameState, depth: int, alpha: int, beta: int) -> int:
        v = -np.inf
        for action in self.get_actions(state):
            v = max(v, self.minimax(self.update_board(state, action), depth + 1, alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v

    def min_value(self, state: GameState, depth: int, alpha: int, beta: int) -> int:
        v = np.inf
        for action in self.get_actions(state):
            v = min(v, self.minimax(self.update_board(state, action), depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v