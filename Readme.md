# AIML-LAB

A collection of classic **Artificial Intelligence** search algorithms and
**Machine Learning** regression techniques, implemented in Python as lab
practicals.

## 📂 Repository Structure

```
AIML-LAB/
├── 8puzzle/         # 8-Puzzle solver using search algorithms (BFS/A*)
├── Astar/           # A* Search Algorithm for shortest-path problems
├── TSP.py           # Travelling Salesman Problem (brute-force solver)
├── Water Jug/        # Water Jug Problem solved with DFS
├── hillclimbing/    # Hill Climbing algorithm implementation
├── questions/       # Lab questions / problem statements
├── ridgeandlasso/   # Ridge and Lasso regression (ML)
└── Readme.md
```

## 🧠 Contents

### AI Search Algorithms

| Folder / File | Description |
|---|---|
| [`Water Jug`](./Water%20Jug) | Solves the classic Water Jug Problem — measuring an exact target volume using two unmarked jugs — via **Depth First Search (DFS)** with a stack and visited-set to avoid cycles. |
| [`8puzzle`](./8puzzle) | Solves the 3×3 sliding tile puzzle by searching the state space (e.g. **BFS** for a guaranteed shortest solution, or **A\*** with a Manhattan-distance heuristic for efficiency). |
| [`hillclimbing`](./hillclimbing) | Implements **Hill Climbing**, a local search technique that repeatedly moves to the best neighboring state until no improving move remains (a local or global optimum). |
| [`Astar`](./Astar) | Implements the **A\* Search Algorithm** (`f(n) = g(n) + h(n)`) to find the optimal shortest path on a weighted graph using an admissible heuristic. |
| [`TSP.py`](./TSP.py) | Solves the **Travelling Salesman Problem** by brute-force enumeration of all city permutations to find the minimum-cost closed tour (NP-hard — exponential time). |

### Machine Learning

| Folder | Description |
|---|---|
| [`ridgeandlasso`](./ridgeandlasso) | Implements **Ridge (L2)** and **Lasso (L1)** regularized linear regression models to handle overfitting and feature selection. |

### Other

| Folder | Description |
|---|---|
| [`questions`](./questions) | Lab problem statements / assignment questions. |

## 🚀 Getting Started

### Prerequisites
- Python 3.x

### Running a script
Clone the repository and run any script directly:

```bash
git clone https://github.com/Yashx0012/AIML-LAB.git
cd AIML-LAB
python TSP.py
```

For folder-based labs (e.g. `Water Jug`, `8puzzle`, `Astar`, `hillclimbing`),
navigate into the folder and run the Python file inside it:

```bash
cd "Water Jug"
python water_jug.py
```

*(Adjust file names above to match the actual script names in each folder.)*

## 📚 Topics Covered

- Uninformed search: **DFS**, **BFS**
- Informed / heuristic search: **A\***
- Local search: **Hill Climbing**
- Classic AI problems: **Water Jug Problem**, **8-Puzzle**, **Travelling
  Salesman Problem**
- Regularized regression: **Ridge Regression**, **Lasso Regression**

## 🎓 About

This repository is a lab practical collection built while studying core
**Artificial Intelligence** search strategies and introductory **Machine
Learning** regression techniques.

## 📝 License

No license specified yet — all rights reserved by default until a license
file is added.