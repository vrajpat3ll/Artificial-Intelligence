from NQueensMod import NQueensSolver, State
import tracemalloc
import time
debug = True  # set this to False if you do want the debug info
N = 8
number = int(input("Enter your roll number: "))
print('-'*40)
searchMethod = int(input(
    "searchMethod:\n  BFS  -> 0\n  DFS  -> 1\n  DFID -> 2\nEnter the Search Method: "))

print('-'*40)
print('\n')

if searchMethod == 0:
    traversalMethod = 'bfs'
elif searchMethod == 1:
    traversalMethod = 'dfs'
elif searchMethod == 2:
    traversalMethod = 'dfid'

solver = NQueensSolver(rollNumber=number, N=N)
startNode = State(number, N)
print('startNode = [')
print(str(startNode) + ']')

if not solver.GoalTest(startNode):
    print('This is not a goal node/state!')
    print('-'*40)
    print('\n')
else:
    print('This is a goal node/state!')
    exit()

print(f"Search Method: {traversalMethod}")

if searchMethod == 2:
    # Start memory tracking
    tracemalloc.start()
    # Take a snapshot before calling DFID
    snapshot1 = tracemalloc.take_snapshot()

    startTime = time.time()

    solution = solver.DFID(startNode, dbg=debug)

    endTime = time.time()

    # Take a snapshot after calling DFID
    snapshot2 = tracemalloc.take_snapshot()
    # Stop memory tracking
    tracemalloc.stop()
    # Compute the difference in memory usage
    memory_stats = snapshot2.compare_to(snapshot1, 'lineno')
    if debug:
        # Print top memory usage lines
        print("\nMemory usage details (Top 10):")
        for stat in memory_stats[:10]:
            print(stat)

    print('This is the solution!')
    print(solution[0])


else:
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()

    startTime = time.time()
    solution = solver.ConfigSearch(
        startNode, traversal=traversalMethod, solution='one', dbg=debug)
    endTime = time.time()

    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()
    memory_stats = snapshot2.compare_to(snapshot1, 'lineno')
    if debug:
        # Print top memory usage lines
        print("\nMemory usage details (Top 10):")
        for stat in memory_stats[:10]:
            print(stat)
    if solution == 'COULD NOT FIND SOLUTION!':
        print(solution)
    else:
        print("Solutions:")
        for sol in solution:
            print(sol)
            print('-'*3*8)

print(f"Number of nodes exapanded: ", solver.nodesExpanded)

print(f"Time it took to solve: {endTime - startTime} s")
