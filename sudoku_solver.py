import numpy as np

def sudoku_solver(sudoku):
    
    ''' First, initialise the domain set of each cell, indexed (row,col), with the values 1-9 '''
    domain = np.full((9, 9), set(range(1, 10)))
    
    ''' Each row, column and box must contain the numbers 1-9. Hence, there are 27 total units.
    Each cell belongs to a 1x9 row, 1x9 column and 1x9 box unit. 
    The dictionaries record all the cells in the same unit as the cell in the key.
    For example, row_unit[(0,0)] will contain all of the cells in the first row of the puzzle '''
    
    row_unit = {(i, j): [] for i in range(9) for j in range(9)}
    col_unit = {(i, j): [] for i in range(9) for j in range(9)}
    box_unit = {(i, j): [] for i in range(9) for j in range(9)}
    
    # For non-empty cells, set their domain == their value
    for i in range(9):
        for j in range(9):
            if sudoku[i,j] != 0:
                domain[i,j] = set([sudoku[i,j]])
            
            #For each cell, add the appropriate cells for the row, col and box unit dictionaries    
            for k in range(9):
                row_unit[(i,j)].append((i, k))
                col_unit[(i,j)].append((k, j))
            box_row = (i // 3) * 3
            box_col = (j // 3) * 3
            for k in range(3):
                for l in range(3):
                    box_unit[(i,j)].append((box_row + k, box_col + l))

    # Create one unit dictionary, where the keys are the cells and the values the members of the 
    # three units the cell is a part of: [row_unit, col_unit, box_unit]
    # The units are tracked because in each unit, every cell must be assigned a value 1-9 without duplicates.
    total_units = {}
    for i in range(9):
        for j in range(9):
            row = row_unit[(i,j)]
            col = col_unit[(i,j)]
            box = box_unit[(i,j)]
            total_units[(i,j)] = [row, col, box]
    
    # The peers of a cell are the cells in the same row,col and box as the cell
    # The peers dictionary can be extrapolated from the total_units dictionary by removing 
    # duplicates by converting the list into a set and back to a list and also removing their own cell index.
    peers = {}
    for i in range(9):
        for j in range(9):
            units = total_units[(i,j)]
            peer_set = set()
            for unit in units:
                for cell in unit:
                    if cell != (i,j):
                        peer_set.add(cell)
            peers[(i,j)] = list(peer_set)            
    
    
    '''If a peer of a cell is assigned a value (domain only has one value), the cell can no longer have that 
    value in its domain. The below function iterates over all the empty cells, checking the domain of its peers 
    and removing the infeasable values for the cell's domain '''
                    
    def constraint_propagation(grid):
        for i in range(9):
            for j in range(9):
                if len(grid[i,j]) != 1:
                    peer_vals = set()
                    neighbors = peers[(i,j)]
                    for p in neighbors:
                        if len(grid[p]) == 1:
                            peer_vals.update(grid[p])
                    grid[i,j]= grid[i,j] - peer_vals
        return grid
    
    
    ''' If there is only one possible place for a value to be in a unit, i.e, a value is only an element of one 
    of the cell's domains, assign the value to that cell'''
    def only_one(grid):
        for index in total_units:
            for each_unit in total_units[index]:
                # Iterate throguh values 1-9 and record which cells in the unit has the value in their domain.
                for number in list(range(1,10)):
                    num_places = [cell for cell in each_unit if number in grid[cell]]
                    # Validity check: it is not possible for a cell to have an empty domain. Return false indicates 
                    # current state unsolvable
                    if len(num_places)==0:
                        return False
                    # if only one location for the number in the unit, assign that number
                    # to the respective cell
                    elif len(num_places)==1:
                        grid[num_places[0]] = {number}
        return grid
    
    ''' Elimination loop records cycles through the above two functions unitl no more logical deductions can be made in the 
    current state of the sudoku'''
    def elim_loop(grid):
        # Stuck = True means the number of cells with a domain length == 1 has not changed after passing the cell domains through the 
        # constraint_propagation and only_ones functions
        stuck = False
        while not stuck:
            # Solved pre/post = number of assigned cells (domain length ==1) before/after the current iteration 
            solved_pre = 0
            for i in range(9):
                for j in range(9):
                    if len(grid[i,j]) == 1:
                        solved_pre += 1  
            grid = constraint_propagation(grid)
            grid = only_one(grid)
            # If domain length == 0 for any cell, current state unsolvable 
            if np.any(grid) == False:
                return False
            solved_post = 0
            for i in range(9):
                for j in range(9):
                    if len(grid[i,j]) == 1:
                        solved_post += 1   
            stuck = solved_pre == solved_post
            # If the cycle does not update any cells in domain, set stuck to True
            
        return grid
    
    ''' Function removes the sets from the domain, outputing the solved sudoku in correct format'''
    def output(d):
        return np.array([[int(cell.pop()) for cell in row] for row in d])
    
    def search(grid):
        
        grid = elim_loop(grid)
        if grid is False:
            return False
        
        # If every cell is is different from zero and has only one possible 
        # value per cell, conclude the algorithm is solved. Return the solution
        count = 0
        for i in range(9):
            for j in range(9):
                if len(grid[i,j]) == 1:
                    count += 1
            if count == 81:
                return output(grid)
        
        #If the elim_loop() is stuck, the algorithm employs dfs, choosing the cells
        # with the smallest domains first
        min_size = 10
        min_index = None
        for i in range(9):
            for j in range(9):
                if len(grid[i,j]) > 1:
                    domain_size = len(grid[i,j])
                    if domain_size < min_size:
                        min_size = domain_size
                        min_index = (i,j)
        
        # test each value for the cell's domain to find the solution        
        for val in grid[min_index]:
            # Save current domain so it can be backstracked to if needed
            new_grid = grid.copy()
            # Assign val to domain[cell] and check if solution found
            new_grid[min_index] = {val}
            
            # The recursion step. With the assumed value for the cell, the algorithm repeats to see
            # if adding this cell leads to a solution. 
            # When current state is unsolvable, the loop continues, testing the next value for the cell in the iteration 
            attempt_solve = search(new_grid)
            
            # If successful, end loop and return solved sudoku
            if np.any(attempt_solve):
                return attempt_solve
        
            
    #Return the solved puzzle if the algorithm could solve it, else return 9x9 matrix of -1s. 
    solved = search(domain)   
    if solved is not None and np.any(solved) != False:
        return solved
    else:
        return np.full((9, 9), -1)  