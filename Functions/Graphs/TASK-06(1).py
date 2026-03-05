import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import Button, RadioButtons
import numpy as np
import heapq
import time
import random
import math

# --- Constants & Colors ---
# 0:Empty, 1:Wall, 2:Start, 3:End, 4:Open, 5:Closed, 6:Path, 7:Agent
COLORS = ['white', 'black', 'orange', 'turquoise', 'yellow', 'red', 'green', 'blue']
CMAP = mcolors.ListedColormap(COLORS)
NORM = mcolors.BoundaryNorm(np.arange(-0.5, 8.5, 1), CMAP.N)

class PathfindingApp:
    def __init__(self):
        self.rows = 20
        self.algo_type = "A*"
        self.h_type = "Manhattan"
        self.dynamic_mode = False
        
        self.reset_state()
        self.setup_ui()
        self.timer = self.fig.canvas.new_timer(interval=150)
        self.timer.add_callback(self.agent_step)

    def reset_state(self):
        self.grid = np.zeros((self.rows, self.rows), dtype=int)
        self.start = (0, 0)
        self.end = (self.rows - 1, self.rows - 1)
        self.open_set, self.closed_set, self.path = set(), set(), []
        self.agent_active = False
        self.agent_pos = None
        self.agent_path = []
        self.agent_idx = 0
        self.dragging = None

    def setup_ui(self):
        self.fig = plt.figure(figsize=(12, 7))
        self.fig.canvas.manager.set_window_title("Dynamic Pathfinding Agent")
        
        # Grid Axes
        self.ax_grid = self.fig.add_axes([0.05, 0.05, 0.65, 0.9])
        self.ax_grid.set_xticks([]); self.ax_grid.set_yticks([])
        self.img = self.ax_grid.imshow(self.get_render_grid(), cmap=CMAP, norm=NORM)
        
        # Connect Mouse Events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

        # UI Widgets (Buttons and RadioButtons)
        ax_algo = self.fig.add_axes([0.75, 0.8, 0.2, 0.1])
        self.radio_algo = RadioButtons(ax_algo, ('A*', 'GBFS'))
        self.radio_algo.on_clicked(self.set_algo)

        ax_heur = self.fig.add_axes([0.75, 0.65, 0.2, 0.1])
        self.radio_heur = RadioButtons(ax_heur, ('Manhattan', 'Euclidean'))
        self.radio_heur.on_clicked(self.set_heur)

        ax_mode = self.fig.add_axes([0.75, 0.5, 0.2, 0.1])
        self.radio_mode = RadioButtons(ax_mode, ('Static', 'Dynamic'))
        self.radio_mode.on_clicked(self.set_mode)

        self.btn_start = Button(self.fig.add_axes([0.75, 0.4, 0.2, 0.05]), 'START SEARCH & MOVE')
        self.btn_start.on_clicked(self.start_search)

        self.btn_maze = Button(self.fig.add_axes([0.75, 0.33, 0.2, 0.05]), 'Gen Maze 30%')
        self.btn_maze.on_clicked(self.gen_maze)

        self.btn_clear = Button(self.fig.add_axes([0.75, 0.26, 0.2, 0.05]), 'Clear Grid')
        self.btn_clear.on_clicked(self.clear_grid)

        self.btn_inc = Button(self.fig.add_axes([0.86, 0.19, 0.09, 0.05]), 'Grid +')
        self.btn_inc.on_clicked(lambda e: self.change_grid(5))
        
        self.btn_dec = Button(self.fig.add_axes([0.75, 0.19, 0.09, 0.05]), 'Grid -')
        self.btn_dec.on_clicked(lambda e: self.change_grid(-5))

        # Metrics Text
        self.metrics_text = self.fig.text(0.75, 0.05, "Metrics:\nTime: 0.0 ms\nVisited: 0\nCost: 0", 
                                          fontsize=12, bbox=dict(facecolor='lightgrey', alpha=0.5))

    # --- Widget Callbacks ---
    def set_algo(self, label): self.algo_type = label
    def set_heur(self, label): self.h_type = label
    def set_mode(self, label): self.dynamic_mode = (label == 'Dynamic')
    
    def change_grid(self, delta):
        new_rows = self.rows + delta
        if 10 <= new_rows <= 50:
            self.rows = new_rows
            self.reset_state()
            self.update_render()

    def gen_maze(self, event):
        self.reset_state()
        self.grid = np.random.choice([0, 1], size=(self.rows, self.rows), p=[0.7, 0.3])
        self.grid[self.start], self.grid[self.end] = 0, 0
        self.update_render()

    def clear_grid(self, event):
        self.reset_state()
        self.update_render()

    # --- Mouse Dragging Logic ---
    def get_cell(self, event):
        if event.inaxes != self.ax_grid: return None
        return int(round(event.ydata)), int(round(event.xdata))

    def on_press(self, event):
        cell = self.get_cell(event)
        if not cell: return
        
        if cell == self.start: self.dragging = 'start'
        elif cell == self.end: self.dragging = 'end'
        elif event.button == 1: self.dragging = 'wall'; self.modify_cell(cell, 1) # Left click
        elif event.button == 3: self.dragging = 'erase'; self.modify_cell(cell, 0) # Right click

    def on_drag(self, event):
        if not self.dragging: return
        cell = self.get_cell(event)
        if not cell: return
        
        if self.dragging == 'start' and cell != self.end and self.grid[cell] == 0:
            self.start = cell
        elif self.dragging == 'end' and cell != self.start and self.grid[cell] == 0:
            self.end = cell
        elif self.dragging == 'wall': self.modify_cell(cell, 1)
        elif self.dragging == 'erase': self.modify_cell(cell, 0)
        self.update_render()

    def on_release(self, event): self.dragging = None

    def modify_cell(self, cell, val):
        if cell != self.start and cell != self.end:
            self.grid[cell] = val
            self.update_render()

    # --- Rendering System ---
    def get_render_grid(self):
        render = np.copy(self.grid)
        for r, c in self.open_set: render[r, c] = 4
        for r, c in self.closed_set: render[r, c] = 5
        for r, c in self.path: render[r, c] = 6
        render[self.start] = 2
        render[self.end] = 3
        if self.agent_active and self.agent_pos:
            render[self.agent_pos] = 7
        return render

    def update_render(self):
        self.img.set_data(self.get_render_grid())
        self.img.set_extent([-0.5, self.rows-0.5, self.rows-0.5, -0.5])
        self.fig.canvas.draw_idle()

    # --- Search Algorithms & Agent ---
    def heuristic(self, p1, p2):
        if self.h_type == "Manhattan": return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def run_search(self, start_pos):
        start_time = time.perf_counter()
        count = 0
        open_queue = []
        heapq.heappush(open_queue, (0, count, start_pos))
        came_from, g_score = {}, {start_pos: 0}
        open_hash, closed_set = {start_pos}, set()

        while open_queue:
            current = heapq.heappop(open_queue)[2]
            open_hash.remove(current)

            if current == self.end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path, closed_set, open_hash, (time.perf_counter() - start_time) * 1000

            closed_set.add(current)

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + dr, current[1] + dc)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.rows and self.grid[neighbor] == 0:
                    
                    if self.algo_type == "A*":
                        temp_g = g_score[current] + 1
                        if temp_g < g_score.get(neighbor, float('inf')):
                            came_from[neighbor] = current
                            g_score[neighbor] = temp_g
                            f_score = temp_g + self.heuristic(neighbor, self.end)
                            if neighbor not in open_hash:
                                count += 1
                                heapq.heappush(open_queue, (f_score, count, neighbor))
                                open_hash.add(neighbor)
                                
                    elif self.algo_type == "GBFS":
                        if neighbor not in closed_set and neighbor not in open_hash:
                            came_from[neighbor] = current
                            h_val = self.heuristic(neighbor, self.end)
                            count += 1
                            heapq.heappush(open_queue, (h_val, count, neighbor))
                            open_hash.add(neighbor)

        return None, closed_set, open_hash, (time.perf_counter() - start_time) * 1000

    def start_search(self, event):
        self.open_set, self.closed_set, self.path = set(), set(), []
        path, closed, opens, exec_time = self.run_search(self.start)
        
        self.closed_set, self.open_set = closed, opens
        if path:
            self.path = path
            self.metrics_text.set_text(f"Metrics:\nTime: {exec_time:.2f} ms\nVisited: {len(closed)}\nCost: {len(path)}")
            self.agent_path = path
            self.agent_idx = 0
            self.agent_pos = self.start
            self.agent_active = True
            self.timer.start()
        else:
            self.metrics_text.set_text(f"Metrics:\nTime: {exec_time:.2f} ms\nVisited: {len(closed)}\nCost: No Path")
        self.update_render()

    def agent_step(self):
        if not self.agent_active:
            self.timer.stop(); return

        if self.agent_idx < len(self.agent_path):
            self.agent_pos = self.agent_path[self.agent_idx]

            # Dynamic Mode: Randomly spawn walls
            if self.dynamic_mode and random.random() < 0.15:
                empty = np.argwhere(self.grid == 0)
                valid = [tuple(c) for c in empty if tuple(c) not in (self.start, self.end, self.agent_pos)]
                if valid:
                    new_wall = random.choice(valid)
                    self.grid[new_wall] = 1
                    
                    # If wall blocks the path ahead, replan
                    if new_wall in self.agent_path[self.agent_idx:]:
                        path, closed, opens, t = self.run_search(self.agent_pos)
                        if path:
                            self.path, self.closed_set, self.open_set = path, closed, opens
                            self.agent_path = path
                            self.agent_idx = 0
                            self.metrics_text.set_text(f"Metrics (Replanned):\nTime: {t:.2f} ms\nVisited: {len(closed)}\nCost: {len(path)}")
                        else:
                            self.metrics_text.set_text("Agent Trapped!")
                            self.agent_active = False

            self.agent_idx += 1
            self.update_render()
        else:
            self.agent_active = False
            self.timer.stop()

if __name__ == "__main__":
    app = PathfindingApp()
    plt.show()