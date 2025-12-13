# predator_prey_a_star.py
import random
import heapq
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap


# --- Cell states ---
EMPTY = 0
RABBIT = 1
WOLF = 2


def neighbors4_idx(y: int, x: int, h: int, w: int):
    if y > 0:
        yield (y - 1, x)
    if y < h - 1:
        yield (y + 1, x)
    if x > 0:
        yield (y, x - 1)
    if x < w - 1:
        yield (y, x + 1)


def manhattan(a, b) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid: np.ndarray, start, goal, h: int, w: int):
    """
    A* on grid (4-neighborhood).
    Passable: EMPTY or RABBIT cells; WOLF cells are obstacles (except start).
    Returns path as list of (y,x) from start to goal, or None.
    """
    if start == goal:
        return [start]

    def passable(y: int, x: int) -> bool:
        if (y, x) == start:
            return True
        return grid[y, x] != WOLF

    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            # Reconstruct
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        cy, cx = current
        for ny, nx in neighbors4_idx(cy, cx, h, w):
            if not passable(ny, nx):
                continue

            tentative = g_score[current] + 1
            if (ny, nx) not in g_score or tentative < g_score[(ny, nx)]:
                came_from[(ny, nx)] = current
                g_score[(ny, nx)] = tentative
                f = tentative + manhattan((ny, nx), goal)
                heapq.heappush(open_heap, (f, (ny, nx)))

    return None


@dataclass
class WorldConfig:
    width: int = 60
    height: int = 40
    n_rabbits: int = 200
    n_wolves: int = 40
    p_rabbit_birth: float = 0.05
    seed: int = 42

    wolf_energy_init: int = 8
    wolf_energy_gain: int = 6
    wolf_energy_max: int = 20

    wolf_vision_radius: int = 12  # if nearest rabbit is farther, wolf random-walks


class World:
    def __init__(self, cfg: WorldConfig):
        self.cfg = cfg
        self.width = cfg.width
        self.height = cfg.height

        random.seed(cfg.seed)
        np.random.seed(cfg.seed)

        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.wolf_energy = np.zeros((self.height, self.width), dtype=np.int16)

        self._spawn_random(cfg.n_rabbits, cfg.n_wolves)

    def _spawn_random(self, n_rabbits: int, n_wolves: int):
        cells = [(y, x) for y in range(self.height) for x in range(self.width)]
        random.shuffle(cells)

        for _ in range(n_rabbits):
            if not cells:
                break
            y, x = cells.pop()
            self.grid[y, x] = RABBIT

        for _ in range(n_wolves):
            if not cells:
                break
            y, x = cells.pop()
            if self.grid[y, x] == EMPTY:
                self.grid[y, x] = WOLF
                self.wolf_energy[y, x] = self.cfg.wolf_energy_init

    def count_populations(self):
        return int(np.sum(self.grid == RABBIT)), int(np.sum(self.grid == WOLF))

    def mean_wolf_energy(self) -> float:
        mask = (self.grid == WOLF)
        return float(np.mean(self.wolf_energy[mask])) if np.any(mask) else 0.0

    def _pick_target_rabbit(self, wolf_pos, rabbit_positions, eaten):
        wy, wx = wolf_pos
        best = None
        best_d = None
        for ry, rx in rabbit_positions:
            if eaten[ry, rx]:
                continue
            d = abs(wy - ry) + abs(wx - rx)
            if best is None or d < best_d:
                best = (ry, rx)
                best_d = d
        return best, best_d

    def _random_wolf_step(self, old_grid, new_grid, wy, wx, energy):
        energy -= 1
        if energy <= 0:
            return None

        neigh = list(neighbors4_idx(wy, wx, self.height, self.width))
        random.shuffle(neigh)

        for ny, nx in neigh:
            if old_grid[ny, nx] != WOLF and new_grid[ny, nx] == EMPTY:
                new_grid[ny, nx] = WOLF
                return (ny, nx, energy)

        if new_grid[wy, wx] == EMPTY:
            new_grid[wy, wx] = WOLF
            return (wy, wx, energy)

        return None

    def _move_wolves(self, old_grid, old_energy):
        h, w = self.height, self.width
        new_grid = np.zeros((h, w), dtype=np.int8)
        new_energy = np.zeros((h, w), dtype=np.int16)
        eaten = np.zeros((h, w), dtype=bool)

        wolf_positions = list(zip(*np.where(old_grid == WOLF)))
        rabbit_positions = list(zip(*np.where(old_grid == RABBIT)))

        for wy, wx in wolf_positions:
            energy = int(old_energy[wy, wx])
            if energy <= 0:
                energy = self.cfg.wolf_energy_init

            if not rabbit_positions:
                res = self._random_wolf_step(old_grid, new_grid, wy, wx, energy)
                if res:
                    y2, x2, e2 = res
                    new_energy[y2, x2] = e2
                continue

            target, dist = self._pick_target_rabbit((wy, wx), rabbit_positions, eaten)
            if target is None:
                res = self._random_wolf_step(old_grid, new_grid, wy, wx, energy)
                if res:
                    y2, x2, e2 = res
                    new_energy[y2, x2] = e2
                continue

            # Hybrid: if too far, don't A*
            if dist is not None and dist > self.cfg.wolf_vision_radius:
                res = self._random_wolf_step(old_grid, new_grid, wy, wx, energy)
                if res:
                    y2, x2, e2 = res
                    new_energy[y2, x2] = e2
                continue

            path = a_star(old_grid, (wy, wx), target, h, w)
            if path is None or len(path) < 2:
                res = self._random_wolf_step(old_grid, new_grid, wy, wx, energy)
                if res:
                    y2, x2, e2 = res
                    new_energy[y2, x2] = e2
                continue

            ny, nx = path[1]

            # Eat rabbit
            if old_grid[ny, nx] == RABBIT and not eaten[ny, nx]:
                eaten[ny, nx] = True
                energy = min(self.cfg.wolf_energy_max, energy + self.cfg.wolf_energy_gain)

                if new_grid[ny, nx] == EMPTY:
                    new_grid[ny, nx] = WOLF
                    new_energy[ny, nx] = energy
                else:
                    if new_grid[wy, wx] == EMPTY:
                        new_grid[wy, wx] = WOLF
                        new_energy[wy, wx] = energy
            else:
                # Normal move costs energy
                energy -= 1
                if energy <= 0:
                    continue

                if new_grid[ny, nx] == EMPTY:
                    new_grid[ny, nx] = WOLF
                    new_energy[ny, nx] = energy
                else:
                    if new_grid[wy, wx] == EMPTY:
                        new_grid[wy, wx] = WOLF
                        new_energy[wy, wx] = energy

        return new_grid, new_energy, eaten

    def _move_rabbits(self, old_grid, wolves_grid, eaten):
        h, w = self.height, self.width
        new_grid = wolves_grid.copy()

        rabbit_positions = list(zip(*np.where(old_grid == RABBIT)))

        for y, x in rabbit_positions:
            if eaten[y, x]:
                continue

            neigh = list(neighbors4_idx(y, x, h, w))
            move_candidates = [(ny, nx) for (ny, nx) in neigh if new_grid[ny, nx] == EMPTY]

            if move_candidates:
                ty, tx = random.choice(move_candidates)
            else:
                ty, tx = y, x

            if new_grid[ty, tx] != EMPTY:
                continue

            new_grid[ty, tx] = RABBIT

            # Reproduction
            if random.random() < self.cfg.p_rabbit_birth:
                repro_candidates = [(ny, nx) for (ny, nx) in neigh if new_grid[ny, nx] == EMPTY]
                if repro_candidates:
                    ry, rx = random.choice(repro_candidates)
                    new_grid[ry, rx] = RABBIT

        return new_grid

    def step(self):
        old_grid = self.grid.copy()
        old_energy = self.wolf_energy.copy()

        wolves_grid, wolves_energy, eaten = self._move_wolves(old_grid, old_energy)
        final_grid = self._move_rabbits(old_grid, wolves_grid, eaten)

        self.grid = final_grid
        self.wolf_energy = wolves_energy

        return self.count_populations()


def main():
    cfg = WorldConfig()
    world = World(cfg)

    # --- UI state ---
    running = True
    steps_per_frame = 1
    interval_ms = 100

    hist_r, hist_w, hist_e = [], [], []
    step_counter = 0

    def snapshot():
        r, w = world.count_populations()
        e = world.mean_wolf_energy()
        hist_r.append(r)
        hist_w.append(w)
        hist_e.append(e)

    snapshot()

    # --- Plot ---
    cmap = ListedColormap(["white", "green", "red"])
    fig, (ax_grid, ax_plot) = plt.subplots(1, 2, figsize=(12, 5))

    im = ax_grid.imshow(world.grid, cmap=cmap, vmin=0, vmax=2)
    ax_grid.set_xticks([])
    ax_grid.set_yticks([])

    (line_r,) = ax_plot.plot([], [], label="Rabbits")
    (line_w,) = ax_plot.plot([], [], label="Wolves")
    (line_e,) = ax_plot.plot([], [], label="Mean wolf energy")
    ax_plot.set_xlabel("Step")
    ax_plot.set_ylabel("Value")
    ax_plot.legend(loc="upper right")

    def redraw():
        im.set_data(world.grid)
        r, w = world.count_populations()
        e = world.mean_wolf_energy()

        ax_grid.set_title(
            f"Step {step_counter} | Rabbits={r} | Wolves={w} | Mean wolf energy={e:.2f}\n"
            f"Space: pause/resume | N: step | R: reset | +/-: speed | Esc: quit"
        )

        x = range(len(hist_r))
        line_r.set_data(x, hist_r)
        line_w.set_data(x, hist_w)
        line_e.set_data(x, hist_e)

        ax_plot.relim()
        ax_plot.autoscale_view()

    def do_steps(n: int):
        nonlocal step_counter
        for _ in range(n):
            world.step()
            step_counter += 1
            snapshot()

    def on_key(event):
        nonlocal running, interval_ms, step_counter, hist_r, hist_w, hist_e, world
        if event.key == " ":
            running = not running
        elif event.key in ("n", "N"):
            running = False
            do_steps(1)
            redraw()
            fig.canvas.draw_idle()
        elif event.key in ("r", "R"):
            running = False
            world = World(cfg)
            hist_r, hist_w, hist_e = [], [], []
            step_counter = 0
            snapshot()
            redraw()
            fig.canvas.draw_idle()
        elif event.key == "escape":
            plt.close(fig)
        elif event.key in ("+", "="):  # speed up
            interval_ms = max(10, interval_ms - 10)
            anim.event_source.interval = interval_ms
        elif event.key in ("-", "_"):  # slow down
            interval_ms = min(1000, interval_ms + 10)
            anim.event_source.interval = interval_ms

    fig.canvas.mpl_connect("key_press_event", on_key)

    def update(_frame):
        if running:
            do_steps(steps_per_frame)
            redraw()
        return (im, line_r, line_w, line_e)

    anim = FuncAnimation(fig, update, interval=interval_ms, blit=False, repeat=False)
    redraw()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
