# Soduku-Solver
Constraint propagation with a Minimum Remaining Value heuristic depth first search in Python

### Method
The algorithm combines constraint propagation with a Minimum Remaining Value heuristic depth first search. This algorithm is generally considered one of the most efficient methods for solving sudoku puzzles. The algorithm works as follows:

Constraint propagation 
1.	Iterate over each empty cell. Each empty cell has a domain from 1 to 9. Each cell has a set of 20 peers, cells which reside within the same row, column or box as the cell. If a cell is assigned a value, as in the cell only has one value in its domain, its peers cannot be assigned that value and hence the value is removed from the domain of the peers. 
2.	Loop through each row, column and box of the sudoku, also called units. If there is only one possible placement for a value in the unit, assign it to that cell. In the case of a contradiction, the value is not an element of the domains of any of the cells in the unit, the current domain set is unsolvable. Hence, return false (conclude infeasible solution in current state).
3.	Repeat steps 1 and 2 until the loop gets stuck: no more logical deductions can be made.

Search 
If the constraint propagation loop gets stuck, DFS is employed starting with the empty cell with the smallest domain size. The search loop is as follows:

1.	For the cell with the smallest domain size, iterate over the possible values for the cell from the numbers in its domain.
2.	Save the current domain set in case backtracking required.
3.	Assign the value in the current iteration to that cell.
4.	Enter the new domain into the constraint propagation loop.
a.	If the constraint propagation loop gets stuck, repeat search steps 1-4 for the next cell with the smallest domain size. If a contradiction was found, backtrack and try and the next possible number for the cell. 
b.	If all the cells have only one number in their domains, return the solved sudoku as a numpy array.

### Motivations

The constraint propagation step massively reduces the search space. Logical cell assignments further reduce the domain size of its peers, resulting in some of those cells’ domains reducing to one number, causing those cells to get assigned to a value and so on. Search is only employed when no more logical deductions can be made. 

Ordering cells via the Minimum Remaining Values heuristic decreases the probability of incorrect searches. Consider a sudoku with two cells with the following domains: A: {1,2,3,4,5,6,7}, B:{9,2}. Cell A has 7 different possibilities, giving a 6/7 chance of guessing incorrectly, whereas cell B only has a 50% chance of being wrong. Consequently, search times are drastically reduced with the MRV heuristic. I considered using the Degree heuristic, especially in the event of cells sharing the smallest domain sizes, however the performance benefit to implementation time ratio did not seem justifiable. 

Additionally, I chose to use sets within dictionaries for the domains since sets are mutable and have a smaller time complexity, O(1) in Python relative to lists, O(n), when filtering through domains. Using immutable data structures would require using deepcopies of the domains for backtracking, using more memory space than the built-in python shallow copy method.

Although I did not test this myself, consensus indicated that using iteration instead of recursion would not improve the algorithm’s performance.
![image](https://github.com/arashid9-1/Soduku-Solver/assets/109870775/1af5c0e3-1be9-41b8-bcc2-3d742cc7b19f)

