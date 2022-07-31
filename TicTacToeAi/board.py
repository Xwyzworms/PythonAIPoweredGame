#%%
from matplotlib.pyplot import pcolor
from pygame.gfxdraw import aacircle
from pygame.draw import line
from gameState import TicTacToeState
#from players import MiniMaxPlayer
from window_logic import BoardWindow

CELL_COLORS = [(255, 255, 255), # empty Cell
               (180, 40, 30), # 1st player
               (180, 180, 30) ] # 2nd player

BOARD_COLOR = (20, 30, 10)
GRID_COLOR = (200, 200, 200)

class TicTacToeWindow(BoardWindow):

    """ 
        This is for Game Window Inisialisation
    """

    def __init__(self, cols=3, rows=3, state=None, autoPlayer=None):
        super().__init__(
            title="Tic tac toe",
            state = state or TicTacToeState(),
            autoplayer=autoPlayer,
            cols=cols, rows=rows,
            grid_size=180, cell_padding=9,
            padding_v=0, padding_h=0
        )
    
    def action_for_cell(self, pos):
        return pos.col + pos.row*self._cols
    
    def draw_background(self, screen):
        screen.fill(BOARD_COLOR)
        grid_size = self._grid_size

        # Kedua loop ini Tujuannya buat nxn Grid 
        for i in range(0, self._cols):
            line(screen, GRID_COLOR, (i * grid_size, 0), (i*grid_size, self._rows * grid_size ))
        for j in range(0, self._rows):
            line(screen, GRID_COLOR, (0, j*grid_size), (self._cols * grid_size, j * grid_size))

    def drawX(self, screen, color, rect):
        """ 
            Draw X Ygy
        """
        line(screen, color, (rect.left,rect.top), (rect.left + rect.width, rect.top + rect.height), width=3)
        line(screen, color, (rect.left + rect.width, rect.top), (rect.left, rect.top + rect.height), width=3)

    def drawCircle(self, screen, color, rect):
        radius = int(rect.width / 2)
        center = rect.left + radius, rect.top + radius
        aacircle(screen, *center, radius, color)
        aacircle(screen, *center, radius-2, color)
        aacircle(screen, *center, radius-1, color)

    def draw_cell(self, screen, player, rect):
        pColor = CELL_COLORS[player]
        ## Player 1 Create X
        ## Player 2 Create Circle
        if player == 1:
            self.drawX(screen, pColor, rect)
        elif player == -1:
            self.drawCircle(screen, pColor, rect)
# %%
