For question 4, run the command on terminal:
```python
python SAT_genetic.py
```
Here, we have defined:
- `Fitness Function`(for a creature):  It is the number of clauses that are satisfied by the chromosome/creature of the population 
- `Crossover`(between 2 parents): Used single-point crossover in which we choose a random point in the chromosome and take 1st half from parent1 and 2nd half from parent2

How to use:
- how to give clauses?
    - If a variable is used in the clause, denote it by the number
    - If a variable's complement is used, denote it by -1*number
    - eg. clauses = [
        [1, 2],
        [-2, 3]
    ]
    denote (X1 or X2) and ((not X2) or X3).
- It is possible that we do not get the solution in the first try as it is based on probability, try running it a few times to reach the solution.
- what you can change?
    - populationSize
    - number of generations to run (named generations in the code on line 49)
    - mutationRate