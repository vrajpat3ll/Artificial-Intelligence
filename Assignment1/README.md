# CS-4-15(TO) Assignment-1

## UTILS

- [graph.py](./utils/graph.py) contains a basic implementation of graph data structure for the TSP.
- [agent.py](./utils/agent.py) contains a base class for the problem solver.
- [search.py](./utils/search.py) contains a `SimpleSearch` class for solving the problems.

  - SimpleSearch Contains:

    1. `ConfigSearch (startNode: State)` for solving the configuration problems.
    1. `PlanningSearch (startNode: State, goalNode: State)` for solving the planning problems.
    1. `DFID (startNode: State)` for finding the solution using Depth-First-Iterative-Deepening.

  - It has the implementation of algorithms that are given in the notes. I have taken them from the notes only.

---

## Travelling Salesman Problem

- [TSPMod.py](./TSPMod.py) contains the Agent for solving the Travelling Salesman Problem.

- [TSP.py](./TSP.py) is the main file to run so that we can solve the problem.

- Run the following commmand on the terminal and enter the details accordingly.

```python
python TSP.py
```

- You will have to run it 3 times to get the outputs for BFS, DFS and DFID manually.
- I have used `distanceThreshold` as input for the maximum distance the salesman can travel, so that when I get the distance which is less than this, I treat it as a solution.

---

## N-Queens Problem

- [NQueensMod.py](./NQueensMod.py) contains the Agent for solving the N Queens Problem.

- [NQueens.py](./NQueens.py) is the main file to run so that we can solve the problem.

- Run the following commmand on the terminal and enter the details accordingly.

```python
python NQueens.py
```

- You will have to run it 3 times to get the outputs for BFS, DFS and DFID manually.

---

## FootNotes

### Put `debug = False` on line 3 of [TSP.py](./TSP.py) or line 4 of [NQueens.py](./NQueens.py) if you only want the solution to the problem.
