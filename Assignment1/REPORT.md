# Travelling Salesman Problem

## BFS:
- Time Complexity: 22 nodes are expanded for most of the distance thresholds (MoveGen function is called)
- Space Complexity: about 1.3KB
- Optimality: Yes, BFS does find the optimal solution or the least DistanceCovered.
## DFS:
- Time Complexity: 22 nodes are expanded for most of the distance thresholds (MoveGen function is called)
- Space Complexity: about 1.3KB
- Optimality: it finds the shortest path along with a sub-optimal path.
## DFID:
- Time Complexity: 39 nodes are expanded for the last distance threshold, 22 for the most (MoveGen function is called)
- Space Complexity: 576 B
- Optimality: it also gives both optimal and sub-optimal paths.



# N Queens Problem
## BFS:
- Time Complexity: 52 nodes are expanded (MoveGen function is called) [ 0.0693s ]
- Space Complexity: 54 KiB
- Optimality: Yes, it gives the shortest path to the optimal solution.
## DFS:
- Time Complexity: 41 nodes are expanded (MoveGen function is called) [ 0.0483s ]
- Space Complexity: 42 KiB
- Optimality: It is giving a longer path to get to goal state.
## DFID:
- Time Complexity: 95 nodes are expanded (MoveGen function is called) [ 0.0729s ]
- Space Complexity: 42KiB
- Optimality: It also gives the shortest path to goal state.