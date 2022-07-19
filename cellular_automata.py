from typing import Callable as tCallable;
from typing import List as tList;
from typing import Tuple as tTuple;
from matplotlib import pyplot as plt;
import numpy as np;
from numpy import ndarray;

# This program simulates 2-dimensional cellular automata
# States of cells are int values
# All cells are initialised to 0 when the grid is created

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

        for y in range(self._array.shape[0]):

            line = "";

            for x in range(self._array.shape[1]):

                v = self._array[y, x];
                v_str = str(v) if v != 0 else " ";
                line = line + v_str + "|";

            line = line[:-1];

            output = output + line + "\n"; # Append line to output

            # Row-separator line
            sep_line = "-+" * self._array.shape[0];
            sep_line = sep_line[:-1];
            output = output + sep_line + "\n";
        
        print(output);

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

def main():

    a = Automaton(
        width = 15,
        initial_values = GAME_OF_LIFE_HONEY_FARM_INIT,
        nbhood_width = GAME_OF_LIFE_NB_WIDTH,
        transition = game_of_life_transition
    );

    # Basic console-based interface. Intend to move to matplotlib interface sometime using the numpy array
    while True:
        print("\n" + ("-" * 20) + "\n");
        a.display_on_console();
        input();
        a.next_step();

if __name__ == "__main__":
    main();