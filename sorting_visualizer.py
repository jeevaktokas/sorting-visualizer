"""
Sorting Visualizer — Algorithm Visualizer
==========================================
Algorithms: Bubble Sort, Merge Sort, Quick Sort, Heap Sort
Visualization: Pygame

Author: [Your Name]
GitHub: [Your GitHub]
LinkedIn: [Your LinkedIn]

How to run:
    pip3 install pygame
    python3 sorting_visualizer.py

Controls:
    SPACE       — Sort
    R           — Shuffle / Reset
    1           — Bubble Sort
    2           — Merge Sort
    3           — Quick Sort
    4           — Heap Sort
    +/-         — Increase / decrease speed
    UP/DOWN     — Increase / decrease array size
    ESC         — Quit
"""

from __future__ import annotations
import pygame
import sys
import random
import time
from enum import Enum


# ─────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────

WINDOW_W, WINDOW_H = 1000, 680
PANEL_W  = 220
BAR_AREA_W = WINDOW_W - PANEL_W
BAR_AREA_H = WINDOW_H - 100   # Leave room for status bar
BAR_AREA_X = 0
BAR_AREA_Y = 60

MIN_BARS, MAX_BARS, DEFAULT_BARS = 10, 150, 60
MIN_SPEED, MAX_SPEED, DEFAULT_SPEED = 1, 20, 8

FPS = 60

# Colours
BG          = (248, 250, 252)
PANEL_BG    = (241, 245, 249)
BLACK       = (15,  23,  42)
GRAY        = (100, 116, 139)
WHITE       = (255, 255, 255)
BAR_DEFAULT = (55,  138, 221)
BAR_COMPARE = (226,  75,  74)
BAR_SWAP    = (245, 158,  11)
BAR_SORTED  = (34,  197,  94)
BAR_PIVOT   = (168,  85, 247)
ACCENT      = (99,  102, 241)


class Algorithm(Enum):
    BUBBLE = "Bubble Sort"
    MERGE  = "Merge Sort"
    QUICK  = "Quick Sort"
    HEAP   = "Heap Sort"


# ─────────────────────────────────────────────
#  Sorting Algorithms (generator-based)
# ─────────────────────────────────────────────
#
#  Each algorithm is a Python generator that yields
#  SortFrame objects describing what to highlight.
#  This keeps algorithm logic pure and separate from
#  the rendering / animation layer.

class SortFrame:
    """Snapshot of one animation step."""
    def __init__(
        self,
        array:    list[int],
        compare:  list[int] | None = None,
        swap:     list[int] | None = None,
        sorted_:  list[int] | None = None,
        pivot:    int | None = None,
        comparisons: int = 0,
        swaps:    int = 0,
    ):
        self.array       = array[:]
        self.compare     = compare  or []
        self.swap        = swap     or []
        self.sorted_     = sorted_  or []
        self.pivot       = pivot
        self.comparisons = comparisons
        self.swaps       = swaps


def bubble_sort(arr: list[int]):
    """
    Bubble Sort — O(n²) time, O(1) space.
    Repeatedly swaps adjacent elements that are out of order.
    Simple but inefficient for large arrays.
    """
    a = arr[:]
    n = len(a)
    comparisons = swaps = 0
    sorted_indices = []

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparisons += 1
            yield SortFrame(a, compare=[j, j+1], sorted_=sorted_indices[:],
                            comparisons=comparisons, swaps=swaps)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                yield SortFrame(a, swap=[j, j+1], sorted_=sorted_indices[:],
                                comparisons=comparisons, swaps=swaps)
        sorted_indices.append(n - 1 - i)

    sorted_indices.append(0)
    yield SortFrame(a, sorted_=list(range(n)), comparisons=comparisons, swaps=swaps)


def merge_sort(arr: list[int]):
    """
    Merge Sort — O(n log n) time, O(n) space.
    Divides array in half, recursively sorts, then merges.
    Stable sort — great for linked lists and external sorting.
    """
    a = arr[:]
    comparisons = swaps = 0
    frames = []

    def ms(arr: list[int], l: int, r: int):
        nonlocal comparisons, swaps
        if l >= r:
            return
        m = (l + r) // 2
        ms(arr, l, m)
        ms(arr, m + 1, r)

        L, R = arr[l:m+1], arr[m+1:r+1]
        i = j = 0
        k = l

        while i < len(L) and j < len(R):
            comparisons += 1
            frames.append(SortFrame(arr, compare=[l+i, m+1+j],
                                    comparisons=comparisons, swaps=swaps))
            if L[i] <= R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            swaps += 1
            frames.append(SortFrame(arr, swap=[k],
                                    comparisons=comparisons, swaps=swaps))
            k += 1

        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
            swaps += 1
            frames.append(SortFrame(arr, swap=[k-1],
                                    comparisons=comparisons, swaps=swaps))
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1
            swaps += 1
            frames.append(SortFrame(arr, swap=[k-1],
                                    comparisons=comparisons, swaps=swaps))

    ms(a, 0, len(a) - 1)
    frames.append(SortFrame(a, sorted_=list(range(len(a))),
                             comparisons=comparisons, swaps=swaps))
    yield from frames


def quick_sort(arr: list[int]):
    """
    Quick Sort — O(n log n) avg, O(n²) worst, O(log n) space.
    Picks a pivot and partitions array around it.
    In practice the fastest general-purpose sort.
    Uses last element as pivot (Lomuto partition scheme).
    """
    a = arr[:]
    comparisons = swaps = 0
    frames = []
    sorted_indices: set[int] = set()

    def qs(arr: list[int], l: int, r: int):
        nonlocal comparisons, swaps
        if l >= r:
            sorted_indices.add(l)
            return
        pivot = arr[r]
        i = l - 1

        for j in range(l, r):
            comparisons += 1
            frames.append(SortFrame(arr, compare=[j, r], pivot=r,
                                    sorted_=list(sorted_indices),
                                    comparisons=comparisons, swaps=swaps))
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                frames.append(SortFrame(arr, swap=[i, j], pivot=r,
                                        sorted_=list(sorted_indices),
                                        comparisons=comparisons, swaps=swaps))

        arr[i + 1], arr[r] = arr[r], arr[i + 1]
        swaps += 1
        pi = i + 1
        sorted_indices.add(pi)
        frames.append(SortFrame(arr, swap=[pi, r],
                                sorted_=list(sorted_indices),
                                comparisons=comparisons, swaps=swaps))
        qs(arr, l, pi - 1)
        qs(arr, pi + 1, r)

    qs(a, 0, len(a) - 1)
    frames.append(SortFrame(a, sorted_=list(range(len(a))),
                             comparisons=comparisons, swaps=swaps))
    yield from frames


def heap_sort(arr: list[int]):
    """
    Heap Sort — O(n log n) time, O(1) space.
    Builds a max-heap, then repeatedly extracts the maximum.
    In-place and not stable, but guaranteed O(n log n).
    """
    a = arr[:]
    n = len(a)
    comparisons = swaps = 0
    frames = []
    sorted_indices: set[int] = set()

    def heapify(arr: list[int], size: int, root: int):
        nonlocal comparisons, swaps
        largest = root
        l, r = 2 * root + 1, 2 * root + 2

        comparisons += 1
        frames.append(SortFrame(arr, compare=[root, l if l < size else root],
                                sorted_=list(sorted_indices),
                                comparisons=comparisons, swaps=swaps))

        if l < size and arr[l] > arr[largest]:
            largest = l
        if r < size and arr[r] > arr[largest]:
            largest = r

        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            swaps += 1
            frames.append(SortFrame(arr, swap=[root, largest],
                                    sorted_=list(sorted_indices),
                                    comparisons=comparisons, swaps=swaps))
            heapify(arr, size, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps += 1
        sorted_indices.add(i)
        frames.append(SortFrame(a, swap=[0, i],
                                sorted_=list(sorted_indices),
                                comparisons=comparisons, swaps=swaps))
        heapify(a, i, 0)

    frames.append(SortFrame(a, sorted_=list(range(n)),
                             comparisons=comparisons, swaps=swaps))
    yield from frames


# ─────────────────────────────────────────────
#  Renderer
# ─────────────────────────────────────────────

class Renderer:
    """Handles all Pygame drawing."""

    def __init__(self, screen: pygame.Surface):
        self.screen   = screen
        self.font_sm  = pygame.font.SysFont("monospace", 13)
        self.font_med = pygame.font.SysFont("monospace", 15, bold=True)
        self.font_lg  = pygame.font.SysFont("monospace", 18, bold=True)

    def draw(
        self,
        frame:  SortFrame | None,
        arr:    list[int],
        algo:   Algorithm,
        status: str,
        n_bars: int,
        speed:  int,
    ):
        self.screen.fill(BG)
        self._draw_bars(frame, arr)
        self._draw_header(algo)
        self._draw_panel(frame, algo, n_bars, speed)
        self._draw_status(status)
        pygame.display.flip()

    def _draw_bars(self, frame: SortFrame | None, arr: list[int]):
        if frame:
            data    = frame.array
            compare = set(frame.compare)
            swap    = set(frame.swap)
            sorted_ = set(frame.sorted_)
            pivot   = frame.pivot
        else:
            data = arr; compare = swap = sorted_ = set(); pivot = None

        n      = len(data)
        max_v  = max(data) if data else 1
        bar_w  = max(2, (BAR_AREA_W - n) // n)
        gap    = 1 if bar_w > 3 else 0

        for i, v in enumerate(data):
            x = BAR_AREA_X + i * (bar_w + gap)
            h = max(4, int((v / max_v) * (BAR_AREA_H - 10)))
            y = BAR_AREA_Y + BAR_AREA_H - h

            if i in sorted_:      color = BAR_SORTED
            elif i == pivot:       color = BAR_PIVOT
            elif i in swap:        color = BAR_SWAP
            elif i in compare:     color = BAR_COMPARE
            else:                  color = BAR_DEFAULT

            pygame.draw.rect(self.screen, color, (x, y, bar_w, h), border_radius=2)

    def _draw_header(self, algo: Algorithm):
        pygame.draw.rect(self.screen, WHITE, (0, 0, BAR_AREA_W, 56))
        pygame.draw.line(self.screen, (203, 213, 225), (0, 56), (BAR_AREA_W, 56), 1)
        title = self.font_lg.render("Sorting Visualizer", True, BLACK)
        self.screen.blit(title, (16, 16))
        hint = self.font_sm.render(
            "SPACE=sort  R=shuffle  1-4=algo  +/-=speed  UP/DOWN=size  ESC=quit",
            True, GRAY
        )
        self.screen.blit(hint, (16, 38))

    def _draw_panel(self, frame: SortFrame | None, algo: Algorithm, n_bars: int, speed: int):
        panel = pygame.Rect(BAR_AREA_W, 0, PANEL_W, WINDOW_H)
        pygame.draw.rect(self.screen, PANEL_BG, panel)
        pygame.draw.line(self.screen, (203, 213, 225), (BAR_AREA_W, 0), (BAR_AREA_W, WINDOW_H), 1)

        x, y = BAR_AREA_W + 14, 20

        self._section("ALGORITHM", x, y); y += 22
        for a in Algorithm:
            active = a == algo
            bg = ACCENT if active else WHITE
            fg = WHITE  if active else BLACK
            r  = pygame.Rect(x, y, PANEL_W - 28, 26)
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            if not active:
                pygame.draw.rect(self.screen, (203, 213, 225), r, 1, border_radius=4)
            lbl = self.font_sm.render(a.value, True, fg)
            self.screen.blit(lbl, (x + 8, y + 6))
            y += 32

        y += 8
        self._section("STATS", x, y); y += 22
        comp = frame.comparisons if frame else 0
        swps = frame.swaps       if frame else 0
        rows = [
            ("Comparisons", str(comp)),
            ("Swaps",       str(swps)),
            ("Array size",  str(n_bars)),
            ("Speed",       f"{speed}/10"),
        ]
        for label, val in rows:
            self._stat(label, val, x, y); y += 24

        y += 12
        self._section("COMPLEXITY", x, y); y += 22
        complexities = {
            Algorithm.BUBBLE: ("O(n²)",     "O(1)"),
            Algorithm.MERGE:  ("O(n logn)", "O(n)"),
            Algorithm.QUICK:  ("O(n logn)", "O(logn)"),
            Algorithm.HEAP:   ("O(n logn)", "O(1)"),
        }
        tc, sc = complexities[algo]
        self._stat("Time",  tc, x, y); y += 24
        self._stat("Space", sc, x, y); y += 32

        self._section("LEGEND", x, y); y += 22
        legend = [
            (BAR_DEFAULT, "Default"),
            (BAR_COMPARE, "Comparing"),
            (BAR_SWAP,    "Swapping"),
            (BAR_PIVOT,   "Pivot"),
            (BAR_SORTED,  "Sorted"),
        ]
        for color, name in legend:
            pygame.draw.rect(self.screen, color, (x, y + 3, 12, 12), border_radius=2)
            lbl = self.font_sm.render(name, True, GRAY)
            self.screen.blit(lbl, (x + 18, y))
            y += 20

    def _draw_status(self, text: str):
        bar = pygame.Rect(0, WINDOW_H - 30, BAR_AREA_W, 30)
        pygame.draw.rect(self.screen, BLACK, bar)
        lbl = self.font_sm.render(text, True, WHITE)
        self.screen.blit(lbl, (12, WINDOW_H - 22))

    def _section(self, text: str, x: int, y: int):
        lbl = self.font_sm.render(text, True, GRAY)
        self.screen.blit(lbl, (x, y))

    def _stat(self, key: str, val: str, x: int, y: int):
        k = self.font_sm.render(key,  True, GRAY)
        v = self.font_med.render(val, True, BLACK)
        self.screen.blit(k, (x, y))
        self.screen.blit(v, (x + 110, y))


# ─────────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────────

class App:
    """
    Main app — manages state, input, and animation loop.
    Decouples sorting logic (generators) from rendering.
    """

    def __init__(self):
        pygame.init()
        self.screen   = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Sorting Visualizer — DSA Project")
        self.clock    = pygame.time.Clock()
        self.renderer = Renderer(self.screen)

        self.algo   = Algorithm.BUBBLE
        self.n_bars = DEFAULT_BARS
        self.speed  = DEFAULT_SPEED

        self.arr:       list[int]           = []
        self.generator: object | None       = None
        self.cur_frame: SortFrame | None    = None
        self.sorting:   bool                = False
        self.tick:      int                 = 0
        self.status:    str                 = "Press R to shuffle, then SPACE to sort."

        self._new_array()

    # ── Array ──────────────────────────────────

    def _new_array(self):
        self.arr = [random.randint(5, 100) for _ in range(self.n_bars)]
        self.cur_frame = None
        self.sorting   = False
        self.generator = None
        self.status    = "Shuffled! Press SPACE to sort."

    # ── Input ──────────────────────────────────

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                self._on_key(event.key)

    def _on_key(self, key: int):
        if key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()

        elif key == pygame.K_r:
            self._new_array()

        elif key == pygame.K_SPACE:
            if not self.sorting:
                self._start_sort()

        elif key == pygame.K_1: self._set_algo(Algorithm.BUBBLE)
        elif key == pygame.K_2: self._set_algo(Algorithm.MERGE)
        elif key == pygame.K_3: self._set_algo(Algorithm.QUICK)
        elif key == pygame.K_4: self._set_algo(Algorithm.HEAP)

        elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            self.speed = min(MAX_SPEED, self.speed + 1)
            self.status = f"Speed: {self.speed}/{MAX_SPEED}"

        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self.speed = max(MIN_SPEED, self.speed - 1)
            self.status = f"Speed: {self.speed}/{MAX_SPEED}"

        elif key == pygame.K_UP:
            if not self.sorting:
                self.n_bars = min(MAX_BARS, self.n_bars + 10)
                self._new_array()

        elif key == pygame.K_DOWN:
            if not self.sorting:
                self.n_bars = max(MIN_BARS, self.n_bars - 10)
                self._new_array()

    def _set_algo(self, algo: Algorithm):
        if not self.sorting:
            self.algo   = algo
            self.status = f"Selected: {algo.value}. Press SPACE to sort."

    def _start_sort(self):
        algo_map = {
            Algorithm.BUBBLE: bubble_sort,
            Algorithm.MERGE:  merge_sort,
            Algorithm.QUICK:  quick_sort,
            Algorithm.HEAP:   heap_sort,
        }
        self.generator = algo_map[self.algo](self.arr)
        self.sorting   = True
        self.status    = f"Sorting with {self.algo.value}..."

    # ── Animation ──────────────────────────────

    def _tick_sort(self):
        if not self.sorting or self.generator is None:
            return

        steps_per_tick = max(1, self.speed * 2)
        for _ in range(steps_per_tick):
            try:
                self.cur_frame = next(self.generator)
                self.arr = self.cur_frame.array
            except StopIteration:
                self.sorting   = False
                self.generator = None
                comp = self.cur_frame.comparisons if self.cur_frame else 0
                swps = self.cur_frame.swaps       if self.cur_frame else 0
                self.status = (
                    f"{self.algo.value} done — "
                    f"{comp} comparisons, {swps} swaps."
                )
                break

    # ── Main Loop ──────────────────────────────

    def run(self):
        while True:
            self.handle_events()
            self._tick_sort()
            self.renderer.draw(
                frame  = self.cur_frame,
                arr    = self.arr,
                algo   = self.algo,
                status = self.status,
                n_bars = self.n_bars,
                speed  = self.speed,
            )
            self.clock.tick(FPS)


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    App().run()
