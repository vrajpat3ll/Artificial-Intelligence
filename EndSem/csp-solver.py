from copy import deepcopy
class CSP:
    def __init__(self, variables, domains, constraints):
        """
        Initialize CSP solver with AC-1 capability
        variables: list of variables
        domains: dictionary of variable: [possible_values]
        constraints: list of (var1, var2, constraint_func) tuples
        """
        self.variables = variables
        self.domains = deepcopy(domains)  # Make a copy to preserve original domains
        self.constraints = constraints
        self.assignment = {}
        self.constraint_graph = self._build_constraint_graph()

    def _build_constraint_graph(self):
        """Build adjacency list representation of constraint graph"""
        graph = {var: [] for var in self.variables}
        for (var1, var2, _) in self.constraints:
            graph[var1].append(var2)
            graph[var2].append(var1)
        return graph

    def revise(self, x, y):
        """
        Revise the domain of x with respect to y
        Returns True if the domain of x was changed
        """
        revised = False
        constraint_func = None
        
        # Find the relevant constraint function
        for (var1, var2, func) in self.constraints:
            if (var1 == x and var2 == y) or (var2 == x and var1 == y):
                constraint_func = func
                break
                
        if not constraint_func:
            return False

        to_delete = []
        for x_val in self.domains[x]:
            # Check if there exists any value in y's domain that satisfies the constraint
            satisfied = False
            for y_val in self.domains[y]:
                if (var1 == x and constraint_func(x_val, y_val)) or \
                   (var2 == x and constraint_func(y_val, x_val)):
                    satisfied = True
                    break
            
            if not satisfied:
                to_delete.append(x_val)
                revised = True
        
        # Remove inconsistent values
        for x_val in to_delete:
            self.domains[x].remove(x_val)
            
        return revised

    def ac1(self):
        """
        Implement AC-1 algorithm
        Returns False if a domain becomes empty
        """
        while True:
            domain_changed = False
            
            # Check each constraint edge
            for x in self.variables:
                if len(self.domains[x]) == 0:
                    return False
                    
                for y in self.constraint_graph[x]:
                    # Revise in both directions
                    if self.revise(x, y):
                        domain_changed = True
                    if self.revise(y, x):
                        domain_changed = True
                        
            if not domain_changed:
                break
                
        return all(len(self.domains[x]) > 0 for x in self.variables)

    def is_consistent(self, variable, value):
        """Check if assignment is consistent with constraints"""
        self.assignment[variable] = value
        
        for (var1, var2, constraint_func) in self.constraints:
            if var1 == variable and var2 in self.assignment:
                if not constraint_func(value, self.assignment[var2]):
                    del self.assignment[variable]
                    return False
            if var2 == variable and var1 in self.assignment:
                if not constraint_func(self.assignment[var1], value):
                    del self.assignment[variable]
                    return False
        
        del self.assignment[variable]
        return True

    def select_unassigned_variable(self):
        """Select a variable to assign next (MRV heuristic)"""
        unassigned = [v for v in self.variables if v not in self.assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def backtrack(self):
        """Main backtracking search with AC-1 preprocessing"""
        # Run AC-1 as preprocessing step
        if not self.ac1():
            return None
            
        if len(self.assignment) == len(self.variables):
            return self.assignment
        
        var = self.select_unassigned_variable()
        
        for value in self.domains[var]:
            if self.is_consistent(var, value):
                self.assignment[var] = value
                result = self.backtrack()
                if result is not None:
                    return result
                del self.assignment[var]
        
        return None

# Example usage with map coloring problem
def example_csp():
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    domains = {
        'WA': ['red', 'green', 'blue'],
        'NT': ['red', 'green', 'blue'],
        'SA': ['red', 'green', 'blue'],
        'Q': ['red', 'green', 'blue'],
        'NSW': ['red', 'green', 'blue'],
        'V': ['red', 'green', 'blue'],
        'T': ['red', 'green', 'blue'],
    }
    
    def different_colors(color1, color2):
        return color1 != color2
    
    constraints = [
        ('WA', 'NT', different_colors),
        ('WA', 'SA', different_colors),
        ('NT', 'SA', different_colors),
        ('NT', 'Q', different_colors),
        ('SA', 'Q', different_colors),
        ('SA', 'NSW', different_colors),
        ('SA', 'V', different_colors),
        ('Q', 'NSW', different_colors),
        ('NSW', 'V', different_colors),
    ]
    
    csp = CSP(variables, domains, constraints)
    solution = csp.backtrack()
    return solution

if __name__ == "__main__":
    solution = example_csp()
    if solution:
        print("Solution found:")
        for var, value in sorted(solution.items()):
            print(f"{var}: {value}")
    else:
        print("No solution found")
