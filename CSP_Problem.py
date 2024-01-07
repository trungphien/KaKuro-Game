class CSP_Problem():
    def __init__(self):
        self.variables = []
        self.domain = {}
        self.constraints = {}
        self.neighbours = {}
    
    def add_variable(self, x_variable):
        if x_variable not in self.variables:
            self.variables.append(x_variable)
    
    def add_neighbour(self, x_variable, u_variable):
        if x_variable in self.neighbours:
            if u_variable not in self.neighbours[x_variable]:
                self.neighbours[x_variable].append(u_variable)
        else:
            self.neighbours[x_variable] = [u_variable]
    
    def add_domain(self, x_variable, added_domain): 
        if x_variable in self.domain:
            self.domain[x_variable] = list(set(self.domain[x_variable]).intersection(set(added_domain)))
        else: 
            self.domain[x_variable] = added_domain
    
    def add_constraint(self): pass
    
    def order_domain_values(self, variable):
        return self.domain[variable]
    
    def select_unassigned_variable(self, assignment): 
        for variable in self.variables:
            if variable not in assignment:
              return variable
    
    def is_satisfied_constraint(self): pass
    
    def is_consistent(self, variable, value, assignment): pass

    def action(self): pass
    