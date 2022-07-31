from enum import auto
from re import L
from tracemalloc import start
from types import SimpleNamespace
import pygame
from pygame.draw import line


class BoardWindow:

    def __init__(self, state, autoplayer, cols, rows, grid_size, padding_v, padding_h, cell_padding, title):
        """
        This class for all logic that will be run 
        on the game

        Args :
        autoPlayer = AI 
        """        
        self.state = state
        self._autoplayer = autoplayer
        self._rows = rows
        self._cols = cols
        self._grid_size = grid_size
        self._padding_v = padding_v
        self._padding_h = padding_h
        self._cellPadding = cell_padding
        self._initial_state = state
        self._title = title

    def move(self, action):
        """ 
        This for Tic Tac Move ( Such as Which cells should be move)
        """
        state = self.state 
        if action in state.actions():
           state = state.move(action)
           if not state.gameOver() and self._autoplayer:
                action = self._autoplayer.next_action(state)
                state = state.move(action)
        self.state = state

    def reset(self):
        self.state = self._initial_state 

    def showWindow(self, autoplayer=None):
        pygame.init()

        screen = pygame.display.set_mode(
            size = (self._grid_size * self._cols + 2 * self._padding_h,
                    self._grid_size * self._rows + 2 * self._padding_v)
        )
        pygame.display.set_caption(self._title)
        self.draw(screen)
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset()
                    self.draw(screen)
                ## Mouse Button down means the left click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ## Draw the X / O in the cell
                    cell = self.cell_from_mouse_pos()
                    ## Evaluate first wheter the cell is occupied and current state
                    ## is not gameover
                    if (cell and not self.state.gameOver()):
                            action = self.action_for_cell(cell)
                            self.move(action)
                            self.draw(screen)
                            if self.state.gameOver():
                                print(repr(self.state))
                                pygame.quit()
                                return
            pygame.display.update()

    def draw(self, screen):
        self.draw_background(screen)
        for i, value in enumerate(self.state.cells):
            rect = self.rect_for_cell(i)
            self.draw_cell(screen=screen, player=value, rect=rect)
        self.draw_strikes(screen)

    def draw_strikes(self, screen):
        """
        This method for Drawing Line Strikes
        if Someone Win Lel
        Rule going to be [1,2,3]
        """
        for rule, _ in self.state.strikes():
            rect1 = self.rect_for_cell(rule[0])
            rect2 = self.rect_for_cell(rule[-1])
            ## get the start and end position for Dot 
            start_pos = self.center_for_rect(rect1)
            end_pos = self.center_for_rect(rect2)
            ## Draw The Line
            line(screen, 
            start_pos= start_pos, end_pos=end_pos,
            color=(255, 255, 255), width=2)            
    
    def action_for_cell(self, pos):
        ...
    
    def draw_background(self, screen):
        ...
    
    def draw_cell(self, screen, player, rect):
        ...
    
    def isInRow(self, row):
        return 0 <= row < self._cols

    def isInCol(self, col):
        return 0 <= col < self._rows
 
    def cell_from_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        ## For getting the information about The Cell
        ## Get the center
        col, row = x // self._grid_size , y // self._grid_size
        ## kalau nilai dari col dan row itu ada dalam Center of mouse
        if self.isInRow(row) and self.isInCol(col):
            print("inisideInRow")
            return SimpleNamespace(col=col, row=row)
    
    def center_for_rect(self, rect) :
        w_half = int(rect.width / 2)
        ## get Middle Coordinate
        return rect.left + w_half, rect.top + w_half

    def rect_for_cell(self, index) -> SimpleNamespace:
        """
            Create The Rectangle For A Cell
        """   
        row, col = divmod(index, self._cols)
        return SimpleNamespace(
            left = self._padding_h + col*self._grid_size + self._cellPadding,
            top = self._padding_v + row*self._grid_size + self._cellPadding,
            width = self._grid_size - 2*self._cellPadding,
            height = self._grid_size - 2*self._cellPadding
        )
