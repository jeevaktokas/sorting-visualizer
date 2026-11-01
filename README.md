# Sorting Visualizer — DSA Algorithm Visualizer

A Python + Pygame project that visualizes four classic sorting algorithms in real time with live comparison and swap counters.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.x-green) ![Algorithms](https://img.shields.io/badge/Algorithms-Bubble%20%7C%20Merge%20%7C%20Quick%20%7C%20Heap-orange)

## Algorithms Implemented

| Algorithm   | Time (Best) | Time (Avg)  | Time (Worst) | Space  | Stable |
|-------------|-------------|-------------|--------------|--------|--------|
| Bubble Sort | O(n)        | O(n²)       | O(n²)        | O(1)   | Yes    |
| Merge Sort  | O(n log n)  | O(n log n)  | O(n log n)   | O(n)   | Yes    |
| Quick Sort  | O(n log n)  | O(n log n)  | O(n²)        | O(log n)| No   |
| Heap Sort   | O(n log n)  | O(n log n)  | O(n log n)   | O(1)   | No     |

## Features

- Real-time bar chart visualization of sorting progress
- Color-coded states: comparing (red), swapping (amber), sorted (green), pivot (purple)
- Live counters for comparisons and swaps
- Adjustable array size (10–150 elements)
- Adjustable animation speed
- Generator-based architecture — algorithm logic fully decoupled from rendering

## Getting Started

```bash
git clone https://github.com/jeevaktokas/sorting-visualizer.git
cd sorting-visualizer
pip3 install pygame
python3 sorting_visualizer.py
```

## Controls

| Key        | Action                  |
|------------|-------------------------|
| `SPACE`    | Start sorting           |
| `R`        | Shuffle / reset array   |
| `1`        | Bubble Sort             |
| `2`        | Merge Sort              |
| `3`        | Quick Sort              |
| `4`        | Heap Sort               |
| `+` / `-`  | Increase / decrease speed |
| `UP / DOWN`| Increase / decrease array size |
| `ESC`      | Quit                    |

## Key Concepts Demonstrated

- **Generator-based animation** — each algorithm is a Python generator yielding `SortFrame` objects, cleanly separating logic from rendering
- **Time & space complexity** trade-offs between all four algorithms
- **OOP design** — `SortFrame`, `Renderer`, `App` with single responsibilities
- **In-place vs out-of-place** sorting (Heap/Quick vs Merge)
- **Stable vs unstable** sort properties

## License

MIT
