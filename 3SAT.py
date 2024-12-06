import utils.heuristic_search as hs


class ThreeSAT(hs.HeuristicSearch):
    def __init__(self, config_number, num_variables, clauses) -> None:
        super().__init__()
        self.num_variables = num_variables
        self.clauses = clauses
        self.variables = self.get_variable_values(config_number)

    def get_variable_values(self, config_number):
        """
        Converts the config number to a list of boolean variable values.
        """
        # Convert config_number to binary and reverse to match bit positions to variables
        binary_rep = bin(config_number)[2:].zfill(self.num_variables)
        return [True if bit == '1' else False for bit in binary_rep]

    def evaluate_clause(self, clause):
        """
        Evaluates a single clause for the current variable values.
        Clause is a list like [1, -1, 0] which denotes X1 or (not X2).
        """
        for idx, literal in enumerate(clause):
            if literal == 1:  # X_i (True if corresponding variable is True)
                if self.variables[idx]:
                    return True
            # Not X_i (True if corresponding variable is False)
            elif literal == -1:
                if not self.variables[idx]:
                    return True
        return False

    def GoalTest(self, N):
        """
        Evaluates the entire formula which is a list of clauses.
        Each clause is a list of literals like [1, -1, 0].
        Returns True if all clauses evaluate to True.
        """
        self.variables = self.get_variable_values(N)
        for clause in self.clauses:
            if not self.evaluate_clause(clause):
                return False  # If any clause is False, the whole formula is unsatisfied
        return True  # All clauses are True

    def MoveGen(self, number):
        binary_rep = bin(number)[2:].zfill(self.num_variables)
        moves = []
        for i in range(self.num_variables):
            # hamming distance == 1
            change = '0' if binary_rep[i] == '1' else '1'
            newnode = binary_rep[:i] + change + binary_rep[i+1:]
            moves.append(int(newnode, 2))
        return moves

    # satisfied clauses
    def heuristicValue(self, node) -> int | float:
        count = 0
        self.variables = self.get_variable_values(node)
        for clause in self.clauses:
            if self.evaluate_clause(clause):
                count += 1
        return count

for i in range(16):
    startNode = i  # Binary 0110 -> X1=True, X2=False, X3=True, X4=False
    # goalNode = 10
    num_variables = 4

    clauses = [
        [1, 1, 0, 0],  # X1
        [1, 0, 1, 0],  # X2
        [0, 0, 1, 1],  # X3
        [0, 1, 0, -1],  # X4
        [1, 0, 0, 1],  # X4
        [0, 1, 1, 0],  # X4
        [0, 0, 1, -1],  # X4
        [0, 1, 0, 1],  # X4
        [0, -1, 0, 1],  # X4
    ]

    solver = ThreeSAT(startNode, num_variables, clauses)

    solution = solver.HillClimbing(startNode)
    if solution == "COULD NOT FIND SOLUTION!":
        print(solution)
    if isinstance(solution, list) and len(solution) == 0:
        print("NO SOLUTION FOUND!")
    else:
        for answer in solution:
            print(f"{i} {answer=}")
        print('-'*40)
            # print(f"{i=} | {bin(int(answer))[2:].zfill(num_variables)} is the solution!")
# solution = solver.PlanningSearch(startNode, goalNode, traversal='bfs')

# else:
#     print(i, solution, "is the path to solution!")
#     for answer in solution:
#         print(f"{bin(answer)[2:].zfill(num_variables)} is the solution!")


print('-'*70)
for i in range(16):
    print(f"{i} heur={solver.heuristicValue(i)}")