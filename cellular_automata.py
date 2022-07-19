from typing import Callable as tCallable;
from typing import List as tList;
from typing import Tuple as tTuple;
from matplotlib import pyplot as plt;
import numpy as np;
import pygame;
import time;

# This program simulates 2-dimensional cellular automata
# States of cells are int values
# All cells are initialised to 0 when the grid is created

PYGAME_WINDOW_WIDTH = 400;
PYGAME_BACKGROUND_COLOR = (255, 255, 255);

def cell_color_function(v: int) -> tTuple[int, int, int]:

    """Example function used to get an RGB color from a cell's value"""

    r = (1 - (v & 1)) * 255;
    g = (1 - (((v >> 1) & 1))) * 255;
    b = (1 - (((v >> 2) & 1))) * 255;

    return (r, g, b);

class Automaton:

    def __init__(self,
        width: int,
        initial_values: tList[tTuple[tTuple[int, int], int]],
        nbhood_width: int,
        transition: tCallable[[tList[int]], int]):

        # Initialise the array of values

        self._array = np.zeros(shape = (width, width), dtype = int);

        for iv in initial_values:

            coords = iv[0];
            v = iv[1];

            self._array[coords[0], coords[1]] = v;

        # The width of the square of cells centered around the cell being changed which are inputted to the transition function to determine the next state of the selected cell
        assert nbhood_width % 2 == 1;
        self.nb_range = (nbhood_width - 1) // 2;

        # The transition function applied to cells
        self.transition = transition;

    def get_width(self) -> int:
        return self._array.shape[0];

    def next_step(self) -> None:

        """Applies rules once to the Grid"""

        new = np.empty_like(self._array);

        for y in range(new.shape[0]):
            for x in range(new.shape[1]):

                # Check if neighbourhood exceeds grid bounds
                if ((x - self.nb_range < 0)
                    or (x + self.nb_range >= new.shape[0])
                    or (y - self.nb_range < 0)
                    or (y + self.nb_range >= new.shape[1])):

                    # Kill cell
                    new[y, x] = 0;

                else:

                    nbhood = [];

                    for dy in range(-self.nb_range, self.nb_range + 1):
                        for dx in range(-self.nb_range, self.nb_range + 1):
                            nbhood.append(self._array[y+dy, x+dx]);

                    new_state = self.transition(nbhood);
                    new[y, x] = new_state;

        self._array = new;

    def display_on_console(self) -> None:

        output = "";

        for y in range(self.get_width()):

            line = "";

            for x in range(self.get_width()):

                v = self._array[y, x];
                v_str = str(v) if v != 0 else " ";
                line = line + v_str + "|";

            line = line[:-1];

            output = output + line + "\n"; # Append line to output

            # Row-separator line
            sep_line = "-+" * self.get_width();
            sep_line = sep_line[:-1];
            output = output + sep_line + "\n";
        
        print(output);

    def draw_on_pygame_surface(self, surface: pygame.Surface) -> None:

        cell_width = surface.get_width() / self.get_width();
        
        for y in range(self.get_width()):
            for x in range(self.get_width()):

                v = self._array[y, x];
                c = cell_color_function(v);

                pygame.draw.rect(
                    surface = surface,
                    color = c,
                    rect = (
                        x * cell_width,
                        y * cell_width,
                        cell_width,
                        cell_width
                    )
                );

# Conway's game of life

GAME_OF_LIFE_NB_WIDTH = 3;
def game_of_life_transition(nb: tList[int]) -> int:

    self = nb[4];

    alive_nbs = 0;
    for x in nb:
        if x > 0:
            alive_nbs += 1;

    if self != 0:
        alive_nbs -= 1;
        return 1 if (2 <= alive_nbs <= 3) else 0;
    else:
        return 1 if alive_nbs == 3 else 0;

GAME_OF_LIFE_GLIDER_INIT = [
    ((1, 2), 1),
    ((2, 3), 1),
    ((3, 1), 1),
    ((3, 2), 1),
    ((3, 3), 1)
];

GAME_OF_LIFE_HONEY_FARM_INIT = [
    ((7, 4), 1),
    ((7, 5), 1),
    ((7, 6), 1),
    ((7, 7), 1),
    ((7, 8), 1),
    ((7, 9), 1),
    ((7, 10), 1),
];

# Main functions

def run_console_interface(a: Automaton):

    # Basic console-based interface. Intend to move to matplotlib interface sometime using the numpy array
    while True:
        print("\n" + ("-" * 20) + "\n");
        a.display_on_console();
        input();
        a.next_step();

def run_pygame_interface(a: Automaton):

    # Set-up

    pygame.init();

    window = pygame.display.set_mode(size = (PYGAME_WINDOW_WIDTH, PYGAME_WINDOW_WIDTH));
    clock = pygame.time.Clock();

    running = True;

    while running:

        clock.tick(5);

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False;

        window.fill(PYGAME_BACKGROUND_COLOR);

        a.draw_on_pygame_surface(window);

        a.next_step();

        pygame.display.flip();

    pygame.quit();

def main():

    a = Automaton(
        width = 15,
        initial_values = GAME_OF_LIFE_GLIDER_INIT,
        nbhood_width = GAME_OF_LIFE_NB_WIDTH,
        transition = game_of_life_transition
    );

    run_pygame_interface(a);

if __name__ == "__main__":
    main();