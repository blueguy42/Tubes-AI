from typing import Tuple
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import numpy as np


class LocalSearchBot(Bot):
    # Bakal perlu method yg bangkitin semua neighbor
    # Bakal milih neighbor dengan nilai maks atau sama
    # Kalo udah maks iterasi (pas gerak sideway) atau ngga ada neighbor dengan nilai sama atau lebih, maka return current
    MAX_SIDEWAYS = 20

    def __init__(self, num_of_dots: int):
        self.NUMBER_OF_DOTS = num_of_dots
        self.rowLen = num_of_dots - 1
        self.colLen = num_of_dots - 1
        self.turnStep = 0
        # Is bot player 2 (1) or player 1 (-1)
        self.player2Bool = 1

    # Ini hillclimbingnya
    def get_action(self, state: GameState) -> GameAction:
        # Check if bot is player 1 or 2, and set row and column of board.
        # Only checked on first turn.
        if not self.turnStep:
            if not int(np.sum(state.board_status)):
                self.player2Bool = -1
            self.turnStep += 1

        current = state
        possibleActions = self.get_all_possible_actions(current)
        _, action = self.getNeighbor(current, possibleActions)
        return action
    

    
    def is_terminal(self, state: GameState) -> bool:
        return np.all(state.row_status == 1) and np.all(state.col_status == 1)


    
    def get_utility(self, state: GameState) -> int:
        turnofBot = 1
        
        objectiveFuncScore = 0
        for i in range(self.rowLen):
            for j in range(self.colLen):
                rowVal = int(state.board_status[i][j])*self.player2Bool
                
                if abs(rowVal) == 1:
                    objectiveFuncScore += 5
                elif  abs(rowVal) == 2:
                    objectiveFuncScore += 10
                elif abs(rowVal) == 3:
                    objectiveFuncScore -= 25*turnofBot
                elif abs(rowVal) == 4:
                    objectiveFuncScore += 25*rowVal

        return objectiveFuncScore

    # Fungsi ini mengembalikan list GameState semua kemungkinan gerakan di level saat ini
    def get_all_possible_actions(self, state: GameState) -> list:
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

    
    # Fungsi akan mengembalikan neighbor dengan value tertinggi
    def getNeighbor(self, state: GameState, possibleActions: list) -> tuple((GameState, GameAction)):
        value_max = -np.inf
        chosen_neighbor = None
        chosen_action = None
        val = 1
        playerModifier = 1
        # loop actions
        for action in possibleActions:
            new_board_status = state.board_status.copy()
            new_row_status = state.row_status.copy()
            new_col_status = state.col_status.copy()
            new_x = action.position[0]
            new_y = action.position[1]

            

            # Cek apakah jadi kotak 
            if new_y < (self.NUMBER_OF_DOTS-1) and new_x < (self.NUMBER_OF_DOTS-1):
                new_board_status[new_y][new_x] = (abs(new_board_status[new_y][new_x]) + val) * playerModifier

            if action.action_type == "row":
                new_row_status[new_y][new_x] = 1
                if new_y >= 1:
                    new_board_status[new_y-1][new_x] = (abs(new_board_status[new_y-1][new_x]) + val) * playerModifier
            
            if action.action_type == "col":
                new_col_status[new_y][new_x] = 1
                if new_x >= 1:
                    new_board_status[new_y][new_x-1] = (abs(new_board_status[new_y][new_x-1]) + val) * playerModifier
            
            
            
            # hitung nilai utilitas
            this_value = self.get_utility(GameState(new_board_status, new_row_status, new_col_status, not state.player1_turn))
            if this_value >= value_max:
                value_max = this_value
                chosen_neighbor = GameState(new_board_status, new_row_status, new_col_status, not state.player1_turn)
                chosen_action = action

        return chosen_neighbor, chosen_action