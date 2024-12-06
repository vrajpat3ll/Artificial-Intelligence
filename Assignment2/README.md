# Q1

## Problem Analysis
- The implementation models a Diwali festival route planning scenario with:
- A grid-based city map
- Different terrain types (roads, markets, galis, parks)
- Varying movement costs
- Specific stations to visit
- Obstacle avoidance

Key modeling approaches:

- Custom Cell class to represent grid locations
- FestivalGrid to manage grid navigation
- Terrain-based cost penalties
- Stations defined as specific coordinates

## Heuristic Characteristics
- Weighted Manhattan Distance is used
- Uses Manhattan distance as base heuristic
- Multiplies by minimum terrain cost to ensure admissibility
- Provides lower-bound cost estimate without overestimating

## Introduction
A* search is an informed pathfinding algorithm that combines the cost of reaching a node (g-score) with a heuristic estimate of the remaining distance to the goal (h-score). It's particularly effective for navigation problems with varying terrain costs.

### Admissibility Proof

- Always underestimates actual path cost
- Multiplies by minimum terrain cost
- Guarantees A* will find optimal path

## Complexity Analysis
### Time Complexity

- Worst case: O(b^d), where b is branching factor, d is path depth
- Practical performance improved by heuristic guidance
- Heap operations: O(log n)

### Space Complexity

- O(b^d) to store explored and frontier nodes
- Uses priority queue and dictionaries for tracking

### Challenges and Observations
#### Key Challenges

- Handling varied terrain costs
- Avoiding obstacles
- Optimal station visitation sequence
- Maintaining path optimality

#### Unique Observations

- Terrain penalties significantly impact route selection
- Obstacle avoidance requires careful neighbor selection
- Heuristic design critical for efficient pathfinding


---


# Q2

## Heuristic Analysis:

- Guarantees optimal solution finding
- Estimates minimum operations to complete alignment
- Considers length differences and minimum operation costs
- **Admissible**: Never overestimates remaining cost
- Calculates minimum gaps and remaining sequence lengths
- Lower bound ensures no overestimation
- Key Heuristic Features:
    - Uses minimum gap and operation costs
    - Length difference estimation
    - Monotonic property maintained
    - Computationally efficient



## Complexity Analysis:
### Time Complexity: 
- O(m * n * log(m * n))
- State exploration: O(m * n)
- Heap operations: log(m * n)
- m, n = sequence lengths
- A* uses a priority queue, with potential state expansions

### Space Complexity: 
- O(m * n)
- Open list storage
- Closed set tracking
- Path reconstruction requires storing alignment information