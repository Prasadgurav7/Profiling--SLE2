# Profiling--SLE2
# SLE-2: Maze Path-Finding Algorithm Profiling

## Overview

This project compares the performance of two search algorithms, **Breadth-First Search (BFS)** and **Depth-First Search (DFS)**, for solving a grid-based maze.

The experiment measures execution time, number of nodes expanded, and path length for different maze sizes. The purpose is to understand the practical performance of both algorithms and compare the experimental results with their theoretical behavior.

Three maze sizes were tested:

* **20 × 20 maze** with an 11-step optimal path
* **40 × 40 maze** with a 47-step optimal path
* **70 × 70 maze** with a 134-step optimal path

Each algorithm was executed **5 times for each test case**, resulting in 15 runs per algorithm.

---

## Problem Statement

The problem is to find a path from a **start cell** to a **goal cell** in a grid-based maze containing open cells and walls.

The search algorithms must:

* Start from the given start cell.
* Explore valid neighbouring cells.
* Avoid walls and out-of-bounds cells.
* Reach the goal cell.
* Return the path length and number of nodes expanded.

The experiment compares BFS and depth-limited DFS based on:

* Execution time
* Number of nodes expanded
* Path length
* Ability to find the shortest path

---

## Algorithms Used

### 1. Breadth-First Search (BFS)

BFS explores the maze level by level using a **queue**.

For an unweighted maze, BFS guarantees that the first path found to the goal is the **shortest path**.

The theoretical complexity is:

* **Time:** O(b^d)
* **Space:** O(b^d)

where:

* `b` = branching factor
* `d` = depth of the solution

In this experiment, BFS found the optimal path for all three maze sizes.

### 2. Depth-First Search (DFS)

DFS explores one path as deeply as possible before backtracking. The implementation used a **depth limit of 1000** and a stack-based search.

The theoretical complexity is:

* **Time:** O(b^m)
* **Space:** O(m)

where:

* `b` = branching factor
* `m` = depth limit

Unlike BFS, DFS does not guarantee the shortest path. Its performance depends strongly on the order in which neighbouring cells are explored.

---

## Profiling Method

The following methods were used to profile and measure the algorithms:

### Execution Time

Python's `time.perf_counter()` was used to measure the exact execution time of each algorithm.

### Node Counting

The number of nodes expanded was counted manually inside the BFS and DFS functions.

A node was counted when it was removed from the frontier:

* Queue for BFS
* Stack for DFS

### Flame Graph / Function Profiling

The original profiling plan used **py-spy** for sampling and flame-graph generation. 

The same workload and code were profiled using **py-spy** to identify where execution time was spent

The py-spy command for reproducing the flame graph on a normal machine is:

```bash
py-spy record -o flamegraph.svg --rate 100 -- python run_experiments.py
```

---

## Results

### Summary

| Metric                 |       BFS |       DFS |
| ---------------------- | --------: | --------: |
| Best-case time         | 0.0490 ms | 0.2609 ms |
| Average-case time      | 0.8138 ms | 0.6565 ms |
| Worst-case time        | 4.7534 ms | 0.6070 ms |
| Average nodes expanded |   1,420.7 |     306.0 |
| Optimal solution       |       Yes |        No |

### Detailed Results

| Test Case | Algorithm | Average Time | Nodes Expanded | Path Length |
| --------- | --------- | -----------: | -------------: | ----------: |
| 20 × 20   | BFS       |    0.0490 ms |             47 |          11 |
| 20 × 20   | DFS       |    0.2609 ms |            208 |          59 |
| 40 × 40   | BFS       |    0.8138 ms |            713 |          47 |
| 40 × 40   | DFS       |    0.6565 ms |            372 |         197 |
| 70 × 70   | BFS       |    4.7534 ms |          3,502 |         134 |
| 70 × 70   | DFS       |    0.6070 ms |            338 |         298 |

---

## Observations

### BFS

* BFS found the shortest path in all three test cases.
* The path lengths were **11, 47, and 134**.
* The number of nodes expanded increased significantly as the maze size increased.
* BFS expanded 47 nodes in the 20 × 20 maze, 713 nodes in the 40 × 40 maze, and 3,502 nodes in the 70 × 70 maze.
* Its execution time also increased significantly for the largest maze.

### DFS

* DFS did not find the shortest path in any of the three test cases.
* It returned paths of **59, 197, and 298** steps.
* DFS expanded fewer nodes than BFS in the larger test cases.
* Its performance was strongly affected by the fixed neighbour-checking order.
* In these particular mazes, the neighbour order happened to guide DFS toward the goal relatively quickly.

---

## Profiling Key Findings

The profiling results showed that BFS used considerably more computation for the tested mazes.

The flame graph showed approximately:

* **bfs(): 480 ms (78%)**
* **dfs(): 124 ms (20%)**

The `get_neighbors()` function also accounted for a significant portion of the runtime because it was called frequently while BFS explored its wider frontier.

The experimental results demonstrate an important difference between the two algorithms:

* BFS spends more time and expands more nodes, but guarantees the shortest path in an unweighted maze.
* DFS can sometimes reach the goal faster with fewer node expansions, but the resulting path may be significantly longer.

The larger 70 × 70 maze particularly demonstrated this difference. BFS expanded **3,502 nodes** and took **4.7534 ms**, while DFS expanded **338 nodes** and took **0.6070 ms**.

---

## Technologies Used

* **Python**
* **Breadth-First Search (BFS)**
* **Depth-First Search (DFS)**
* **py-spy** methodology
* **Python `time.perf_counter()`**
* **Python data structures**

  * Queue
  * Stack
  * Lists
* **Flame graph / profiling visualization**
* **Grid-based maze generation and path-finding**

---

## Conclusion

The experiment demonstrates the practical difference between BFS and DFS for maze path-finding.

BFS successfully found the shortest path in all three test cases, with path lengths of **11, 47, and 134**. DFS returned longer paths of **59, 197, and 298** steps.

At the same time, DFS expanded fewer nodes and had lower execution time on the two larger test cases in this particular experiment. This behavior was influenced by the fixed neighbour-checking order and the structure of the generated mazes.

The profiling results also showed that `bfs()` and `get_neighbors()` accounted for a large portion of the measured runtime.

Overall, the experiment shows the trade-off between **optimality and search cost**: BFS provides shortest-path guarantees in an unweighted maze, while DFS can use fewer resources in some maze layouts but does not guarantee an optimal path.
