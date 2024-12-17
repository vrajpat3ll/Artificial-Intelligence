from TSPMod import TSPSolver
import tracemalloc  # Import the tracemalloc module for memory tracking

debug = True  # set this to False if you do want the debug info
cities = int(input("Enter the number of cities: "))
number = int(input("Enter your roll number: "))

# The distance threshold is the maximum distance that the salesman can travel (set arbitrarily)
distanceThreshold = int(input("Enter the distance threshold: "))
searchMethod = int(input("Enter 0 for BFS, 1 for DFS and 2 for DFID: "))

print('-'*90)
print('\n'*4)

# State = [startingCity, partialRouteTaken, totalDistanceCoveredSoFar]
# StartingCity : the city from which the salesman starts (which can be any city but for convinience i've taken 1)
# PartialRouteTaken : list of cities that the salesman has visited so far
# TotalDistanceCoveredSoFar : total distance covered by the salesman so far
startState = [4, [4], 0]

threshold = distanceThreshold

solver = TSPSolver(cities, number)

min = 0
max = distanceThreshold
solutions = []

if searchMethod == 0:
    traversal = 'bfs'
elif searchMethod == 1:
    traversal = 'dfs'
elif searchMethod == 2:
    traversal = 'dfid'
print(f"\n\nSearch Method: {traversal}")


# binary search for the threshold to find the minimum distance solution
while min <= max and distanceThreshold > 0:
    distanceThreshold = (min + max) // 2

    solver.nodesExpanded = 0

    if searchMethod == 2:
        # Start memory tracking
        tracemalloc.start()
        # Take a snapshot before calling DFID
        snapshot1 = tracemalloc.take_snapshot()

        path = solver.DFID(
            startState,
            distanceThreshold=distanceThreshold,
            epochs=250,
            dbg=debug,
        )

        # Take a snapshot after calling DFID
        snapshot2 = tracemalloc.take_snapshot()
        # Stop memory tracking
        tracemalloc.stop()
        # Compute the difference in memory usage
        memory_stats = snapshot2.compare_to(snapshot1, 'lineno')
        # Print top memory usage lines
        if debug:
            print("\nMemory usage details (Top 10):")
            for stat in memory_stats[:10]:
                print(stat)

        if len(path) > 0:
            candidates = path[-1]
        else:
            candidates = []

        if candidates != [] and candidates not in solutions:
            solutions.append(candidates)

    else:
        tracemalloc.start()
        snapshot1 = tracemalloc.take_snapshot()

        candidates = solver.ConfigSearch(
            startState,
            traversal=traversal,
            solution='one',
            distanceThreshold=distanceThreshold,
            dbg=debug,
        )

        snapshot2 = tracemalloc.take_snapshot()
        tracemalloc.stop()
        memory_stats = snapshot2.compare_to(snapshot1, 'lineno')
        if debug:
            print("\nMemory usage details (Top 10):")
            for stat in memory_stats[:10]:
                print(stat)

        if candidates != 'COULD NOT FIND SOLUTION!':
            for candidate in candidates:
                if candidate not in solutions:
                    solutions.append(candidate)

    if candidates == [] or candidates == 'COULD NOT FIND SOLUTION!':
        print('-'*90)
        print(f"{min=} {max=} {distanceThreshold=}\n")

        min = distanceThreshold + 1
    else:
        if candidates != []:
            print(f"\n{min=} {max=} {distanceThreshold=}")

        max = distanceThreshold - 1

    print(f"{solver.nodesExpanded=}")

# --------------------------------------------------------------------------------------------------------------------+
# finding the optimal solution from the list of solutions that have distance <= the treshold given by us
minimum = float('inf')
if len(solutions) == 0:
    print(f"No solution found for {distanceThreshold=}")
else:
    print('\n' + '-'*90)
    print(f"All solutions within distance_{threshold=}:\n")
    for sol in solutions:
        print(solutions)

        if sol[2] < minimum:
            optimalSolution = sol
            minimum = sol[2]
    print('\n' + '-'*90)
    print(f"Optimal path: {
        ' <-> '.join(map(str, optimalSolution[1]))} with cost {optimalSolution[2]}")
    print('-'*90)
