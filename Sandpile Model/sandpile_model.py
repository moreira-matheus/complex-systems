# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 14:40:27 2018

@author: USP
"""

import random
from itertools import product

class Cell:
    threshold = 4
    def __init__(self, n_grains=0):
        self.n_grains = n_grains
        self.overflow = False

    def add_grains(self, n_grains=1):
        '''
        Increases the number of grains.
        '''
        self.n_grains += n_grains
        self.overflow = self.n_grains >= Cell.threshold

    def reset(self):
        '''
        Resets the number of grains back to zero.
        '''
        self.n_grains = 0
        self.overflow = False

class Table:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = None

    def fill_randomly(self):
        '''
        Fills the cells with random numbers of grains (lesser than .
        '''
        self.cells = [[Cell(random.randint(0,Cell.threshold-1))\
                      for _ in range(self.n_cols)] for _ in range(self.n_rows)]

    def overflow_cell(self, row, col):
        '''
        Spills grains to the Von Neumann neighborhood.
        '''
        spilt_grains = int(self.cells[row][col].n_grains/4)
        self.cells[row][col].reset()

        # Spill upwards
        self.cells[row-1][col].add_grains(spilt_grains)
        # Spill downwards
        self.cells[row-self.n_rows+1][col].add_grains(spilt_grains)
        # Spill leftwards
        self.cells[row][col-1].add_grains(spilt_grains)
        # Spill rightwards
        self.cells[row][col-self.n_cols+1].add_grains(spilt_grains)

    def overflow_neighborhood(self, row, col):
        '''
        Checks whether there is a new overflow in the Von Neumann neighborhood.
        '''
        up = self.cells[row-1][col].overflow
        down = self.cells[row-self.n_rows+1][col].overflow
        left = self.cells[row][col-1].overflow
        right = self.cells[row][col-self.n_cols+1].overflow

        return (up or down or left or right)

    def check_overflow(self):
        '''
        Checks whether there are cells which have overflown.
        '''
        while True:
            check_again = False

            for i, j in product(range(self.n_rows),range(self.n_cols)):
                if self.cells[i][j].overflow:
                    self.overflow_cell(i,j)
                    check_again = check_again or self.overflow_neighborhood(i,j)
            
            if not check_again:
                break

    def drop_grain(self, row, col):
        '''
        Drops a grain over the selected cell.
        '''
        self.cells[row][col].add_grains()
        self.check_overflow()

    def grains_per_cell(self):
        '''
        Returns the number of grains per cell.
        '''
        table = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_cols):
                row.append(self.cells[i][j].n_grains)
            table.append(row)

        return table

    def print_rows(self):
        '''
        Prints all the number of grains, one row per line.
        '''
        print('\n')
        for row in self.grains_per_cell():
            print(row)
        print('\n')
        print('-'*self.n_cols*4)

if __name__=='__main__':
    tab = Table(4,6)
    tab.fill_randomly()
    tab.print_rows()
    i,j = random.randint(0,3), random.randint(0,5)
    tab.drop_grain(i,j)
    tab.print_rows()
