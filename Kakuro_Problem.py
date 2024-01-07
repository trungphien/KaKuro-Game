import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations
import CSP_Problem as csp

class Kakuro_Problem(csp.CSP_Problem):
    def __init__(self, number_of_rows, number_of_columns, horizontal, vertical):
        csp.CSP_Problem.__init__(self)
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.horizontal = horizontal
        self.vertical = vertical
        self.type_cell = {}
        self.matrices_to_CSP()
    
    def matrices_to_CSP(self):
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                self.type_cell[(i, j)] = 'blank_cell'
        
        #For the horizontal values
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                #Find sum clues
                if self.horizontal[i][j] != "#" and self.horizontal[i][j] != 0:
                    u_variable_name = ("UR", (i, j))
                    self.type_cell[(i, j)] = 'constraint_cell'
                    #Add the constraint variable
                    self.variables.append(u_variable_name)
                    self.neighbours[u_variable_name] = []
                    k = j + 1
                    ct = 0
                    #set the domain, constraints, neighbours and variables of the block
                    while k < self.number_of_columns:
                        if self.horizontal[i][k] == 0:
                            x_variable_name = ("X", (i, k))
                            self.type_cell[(i, k)] = 'value_cell'
                            self.add_variable(x_variable_name)
                            self.add_domain(x_variable_name, [l for l in range(1,min(int(self.horizontal[i][j]),9)+1)])
                            self.add_neighbour(x_variable_name, u_variable_name)
                            self.add_neighbour(u_variable_name, x_variable_name)
                            self.add_binary_constraint(x_variable_name, u_variable_name, ct)
                            ct += 1
                        else:
                            break
                        k += 1
                    self.add_domain(u_variable_name,[lst for lst in permutations([1,2,3,4,5,6,7,8,9],k-j-1) if sum(lst) == int(self.horizontal[i][j])])
                    j = k 
        
        #For the vertical values
        for j in range(self.number_of_columns):
            for i in range(self.number_of_rows):
                #find the sum clues
                if self.vertical[i][j] != "#" and self.vertical[i][j] != 0:
                    u_variable_name = ("UD",(i, j))
                    self.type_cell[(i, j)] = 'constraint_cell'
                    #Add the constraint variable
                    self.variables.append(u_variable_name)
                    self.neighbours[u_variable_name] = []
                    k = i + 1
                    ct = 0
                    #set the domains constraints neighbours variables in block
                    while k < self.number_of_rows:
                        if self.vertical[k][j] == 0:
                            x_variable_name = ("X", (k, j))
                            self.type_cell[(k, j)] = 'value_cell'
                            self.add_variable(x_variable_name)
                            self.add_domain(x_variable_name, [l for l in range(1,min(int(self.vertical[i][j]),9)+1)])
                            self.add_neighbour(x_variable_name, u_variable_name)
                            self.add_neighbour(u_variable_name, x_variable_name)
                            self.add_binary_constraint(x_variable_name, u_variable_name, ct)
                            ct += 1
                        else:
                            break
                        k += 1
                    self.add_domain(u_variable_name, [lst for lst in permutations([1,2,3,4,5,6,7,8,9],k-i-1) if sum(lst) == int(self.vertical[i][j])])
                 
                    i = k
    
    def add_binary_constraint(self, x_variable, u_variable, ct):
        csp.CSP_Problem.add_constraint(self)
        self.constraints[u_variable+x_variable] = ct
    
    def is_satisfied_binary_constraint(self, xi, valueXi, xj, valueXj):
        csp.CSP_Problem.is_satisfied_constraint(self)
        satisfaction = False
        if xj[0][0] == "U": # constraint_variable
            if valueXi == valueXj[self.constraints[xj+xi]]:
                satisfaction = True
        else: # value_variable
            if valueXi[self.constraints[xi+xj]] == valueXj:
                satisfaction = True
        return satisfaction
    
    def is_consistent(self, variable, value, assignment): 
        csp.CSP_Problem.is_consistent(self, variable, value, assignment)
        for neighbour in self.neighbours[variable]:
            if neighbour in assignment:
                if not self.is_satisfied_binary_constraint(variable, value, neighbour, assignment[neighbour]):
                    return False
        return True
    
    def fill_in_value_cells(self, assignment): 
        csp.CSP_Problem.action(self)
        for variable in assignment:
            i, j = variable[1][0], variable[1][1]
            if self.type_cell[(i, j)] == 'value_cell':
                self.horizontal[i][j] = assignment[variable]
                self.vertical[i][j] = assignment[variable] 
                
    
    def show(self, assignment):
        print(assignment)
        
    
    def show_img(self, figsize):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)

        ax.set_xticks(np.arange(-0.5, self.number_of_columns, 1))
        ax.set_yticks(np.arange(-0.5, self.number_of_rows, 1))
        ax.set_xlim([-0.5, self.number_of_columns-0.5])
        ax.set_ylim([-0.5, self.number_of_rows-0.5])
        ax.invert_yaxis()
        ax.grid(which='both', color='black', linestyle='-', linewidth=2)
        
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                if self.type_cell[(i, j)] == 'value_cell': 
                    if self.horizontal[i][j] != 0:
                        ax.text(j, i, self.horizontal[i][j], fontsize=25,color = 'red', ha='center', va='center')
                else:
                    ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=2, edgecolor='black', facecolor='gray'))
                    ax.plot([j-0.5, j+0.5], [i-0.5, i+0.5], color='black', linestyle='-', linewidth=2)
                    if self.type_cell[(i, j)] == 'constraint_cell':
                        if self.horizontal[i][j] != '#':
                            ax.text(j, i, self.horizontal[i][j], fontsize=15, ha='left', va='bottom')
                        if self.vertical[i][j] != '#':
                            ax.text(j, i, self.vertical[i][j], fontsize=15, ha='right', va='top')
        ax.set_title('Kakuro Game Board')
        ax.set_aspect('equal')
        plt.show()

if __name__ == '__main__':
    rows = 5
    columns = 6
    Horizontal = [['#', '#', '#', '#', '#', '#'],
                [4, 0, 0, '#', '#', '#'],
                [10, 0, 0, 0, 0, '#'],
                ['#', 10, 0, 0, 0, 0],
                ['#', '#', '#', 3, 0, 0]]
                
    Vertical = [['#', 3, 6, '#', '#', '#'],
                ['#', 0, 0, 7, 8, '#'],
                ['#', 0, 0, 0, 0, 3],
                ['#', '#', 0, 0, 0, 0],
                ['#', '#', '#', '#', 0, 0]]
    
    kakuro_game = Kakuro_Problem(rows, columns, Horizontal, Vertical)
    kakuro_game.show_img((10, 10))