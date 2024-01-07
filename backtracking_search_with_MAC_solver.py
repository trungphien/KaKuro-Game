from copy import deepcopy
from typing import Type
import Problem_solver as solver
import CSP_Problem as csp

class backtracking_search_with_MAC_solver(solver.Problem_solver):
    def __init__(self):
        solver.Problem_solver.__init__(self)
        
    def train(self, problem: Type[csp.CSP_Problem]):
        solver.Problem_solver.train(self, problem)
        self.csp_problem = problem
    
    def solve(self):
        solver.Problem_solver.solve(self)
        self.__AC_3(self.csp_problem) # first, use AC_3 to reduce domains
        return self.backtracking_search_with_MAC(self.csp_problem)
    
    #The AC-3 algorithm returns false if the domain becomes empty of some variable
    def __AC_3(self, csp, queue=None):
        if queue == None:
            queue = [(xi,xj) for xi in csp.variables for xj in csp.neighbours[xi]]
        while queue:
            xi,xj = queue.pop(0)
            if self.revise(csp, xi, xj):
                if len(csp.domain[xi]) == 0:
                    return False
                #add the neighbour arcs - {xj} in queue if some value is removed
                for neighbour in csp.neighbours[xi]:
                    if neighbour != xj: 
                        queue.append((neighbour, xi))
        return True
  
    def revise(self, csp, xi, xj):
        revised = False
        for valueXi in csp.domain[xi]:
            remove = True
            for valueXj in csp.domain[xj]:
                if csp.is_satisfied_binary_constraint(xi, valueXi, xj, valueXj):
                    remove = False
                    break
            if remove:
                csp.domain[xi].remove(valueXi)
                revised = True
        return revised   

    # Maintaining arc consistency by calling AC-3 with the queue with only arcs of
    #neighbours of variable
    def MAC(self, csp, variable, assignment):
        queue = [(neighbour,variable) for neighbour in csp.neighbours[variable] if neighbour not in assignment]
        return self.__AC_3(csp, queue)
    
    def backtracking_search_with_MAC(self, csp):
        return self.__recursive_backtracking_with_MAC(csp,{})
    
    #recursive backtracking with mac which returns solution or None
    def __recursive_backtracking_with_MAC(self, csp,assignment):
        #If all values assigned then return the assignment
        if len(assignment) == len(csp.variables):
            return assignment
        variable = csp.select_unassigned_variable(assignment)
        for value in csp.order_domain_values(variable):
            if csp.is_consistent(variable, value, assignment):
                #assign a value to variable
                assignment[variable] = value
                #set the domain of variable as the assigned value
                csp.domain[variable] = [value]
                #save the domain
                saved_domain = deepcopy(csp.domain)
                #prune the domain and if no domain is empty
                inferences = self.MAC(csp, variable, assignment)
                if inferences:
                    #recursively call backtracking
                    result = self.__recursive_backtracking_with_MAC(csp,assignment)
                    if result != None:
                        return result
                #restore domain back 
                csp.domain = deepcopy(saved_domain)
                #remove var = value from assignment
                del assignment[variable]
        return None

