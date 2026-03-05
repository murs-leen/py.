import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import heapq
import time

# --- Constants & Configuration ---
GRID_SIZE = 15
DELAY = 0.01  # Animation delay in seconds

# Colors: 0: White, 1: Black (Wall), 2: Green (Start), 3: Red (Target), 4: Cyan (Frontier), 5: Yellow (Explored), 6: Blue (Path)
COLORS = ['white', 'black', 'lime', 'red', 'cyan', 'yellow', 'royalblue']

class Pathfinder:
    def __init__(self, grid_size = GRID_SIZE):

        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))
        self.start = (0, 0)
        self.target = (grid_size - 3, grid_size - 3)
        self.walls = set()
        self._setup_walls()
        
        # Visualization setup
        self.fig, self.ax = plt.subplots(figsize=(8, 8)) 
        self.img = None
        
    def _setup_walls(self):
        # Create some walls for visualization
        for i in range(5, 11):
            self.walls.add((i, 7))
        for j in range(3, 8):
            self.walls.add((5, j))
            
    def get_neighbors(self, node):
        """Returns neighbors in the specific CLOCKWISE order requested."""
        r, c = node
        # Order: Up, Right, Bottom, Bottom-Right, Left, Top-Left
        directions = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if (nr, nc) not in self.walls:
                    neighbors.append((nr, nc))
        return neighbors

    def update_plot(self, frontier=None, explored=None, path=None):
        """Updates the matplotlib grid for real-time animation."""
        plot_data = np.copy(self.grid)
        # Apply walls
        for r, c in self.walls: plot_data[r, c] = 1
        # Apply explored
        if explored:
            for r, c in explored: plot_data[r, c] = 5
        # Apply frontier
        if frontier:
            for r, c in frontier: plot_data[r, c] = 4
        # Apply path
        if path:
            for r, c in path: plot_data[r, c] = 6
            
        plot_data[self.start] = 2
        plot_data[self.target] = 3

        if self.img is None:
            self.img = self.ax.imshow(plot_data, cmap=plt.cm.colors.ListedColormap(COLORS), vmin=0, vmax=6)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        else:
            self.img.set_data(plot_data)
        
        plt.pause(DELAY)

    # --- 1. BFS ---
    def bfs(self):
        queue = deque([self.start])
        visited = {self.start: None}
        explored = set()

        while queue:
            current = queue.popleft()
            if current == self.target: 
                return self.reconstruct_path(visited)
            
            explored.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
            
            self.update_plot(list(queue), explored)
        return None

    # --- 2. DFS ---
    def dfs(self):
        stack = [self.start]
        visited = {self.start: None}
        explored = set()

        while stack:
            current = stack.pop()
            if current == self.target: return self.reconstruct_path(visited)
            
            explored.add(current)
            # Reversing neighbors for stack to maintain clockwise expansion order
            for neighbor in reversed(self.get_neighbors(current)):
                if neighbor not in visited:
                    visited[neighbor] = current
                    stack.append(neighbor)
            
            self.update_plot(stack, explored)
        return None

    # --- 3. UCS ---
    def ucs(self):
        # (cost, node)
        pq = [(0, self.start)]
        visited = {self.start: (0, None)} # node: (cost, parent)
        explored = set()

        while pq:
            cost, current = heapq.heappop(pq)
            if current == self.target: return self.reconstruct_path(visited, is_ucs=True)
            
            if current in explored: continue
            explored.add(current)
            
            for neighbor in self.get_neighbors(current):
                # Diagonal moves (last 2 in list: (1,1) and (-1,-1)) have cost 1.41, others 1
                move_cost = 1.41 if abs(neighbor[0]-current[0]) == 1 and abs(neighbor[1]-current[1]) == 1 else 1
                new_cost = cost + move_cost
                
                if neighbor not in visited or new_cost < visited[neighbor][0]:
                    visited[neighbor] = (new_cost, current)
                    heapq.heappush(pq, (new_cost, neighbor))
            
            self.update_plot([n for c, n in pq], explored)
        return None

    # --- 4. DLS & 5. IDDFS ---
    def dls(self, limit, animate=True):
        stack = [(self.start, 0)]
        visited = {self.start: None}
        depths = {self.start: 0}
        explored = set()

        while stack:
            current, depth = stack.pop()
            if current == self.target: return self.reconstruct_path(visited)
            
            if depth < limit:
                explored.add(current)
                for neighbor in reversed(self.get_neighbors(current)):
                    if neighbor not in visited or depths[neighbor] > depth + 1:
                        visited[neighbor] = current
                        depths[neighbor] = depth + 1
                        stack.append((neighbor, depth + 1))
                
                if animate: self.update_plot([n for n, d in stack], explored)
        return None

    def iddfs(self):
        for limit in range(self.grid_size * self.grid_size):
            self.ax.set_title(f"IDDFS - Current Depth Limit: {limit}")
            result = self.dls(limit)
            if result: return result
        return None

    # --- 6. Bidirectional Search ---
    def bidirectional(self):
        f_queue, b_queue = deque([self.start]), deque([self.target])
        f_visited, b_visited = {self.start: None}, {self.target: None}
        f_explored, b_explored = set(), set()

        while f_queue and b_queue:
            # Forward step
            curr_f = f_queue.popleft()
            f_explored.add(curr_f)
            if curr_f in b_visited: return self.reconstruct_bidir(f_visited, b_visited, curr_f)
            
            for n in self.get_neighbors(curr_f):
                if n not in f_visited:
                    f_visited[n] = curr_f
                    f_queue.append(n)
            
            # Backward step
            curr_b = b_queue.popleft()
            b_explored.add(curr_b)
            if curr_b in f_visited: return self.reconstruct_bidir(f_visited, b_visited, curr_b)
            
            for n in self.get_neighbors(curr_b):
                if n not in b_visited:
                    b_visited[n] = curr_b
                    b_queue.append(n)
            
            self.update_plot(list(f_queue) + list(b_queue), f_explored.union(b_explored))
        return None

    def reconstruct_path(self, visited, is_ucs=False):
        path = []
        curr = self.target
        while curr is not None:
            path.append(curr)
            curr = visited[curr][1] if is_ucs else visited[curr]
        return path[::-1]

    def reconstruct_bidir(self, f_vis, b_vis, meet_node):
        path_f, path_b = [], []
        curr = meet_node
        while curr:
            path_f.append(curr)
            curr = f_vis[curr]
        curr = b_vis[meet_node]
        while curr:
            path_b.append(curr)
            curr = b_vis[curr]
        return path_f[::-1] + path_b

def main():
    print("Select Algorithm: \n1: BFS\n2: DFS\n3: UCS\n4: DLS (limit=10)\n5: IDDFS\n6: Bidirectional")
    choice = input("Enter choice (1-6): ")
    
    gui = Pathfinder()
    algorithms = {
        '1': ('BFS', gui.bfs),
        '2': ('DFS', gui.dfs),
        '3': ('UCS', gui.ucs),
        '4': ('DLS', lambda: gui.dls(10)),
        '5': ('IDDFS', gui.iddfs),
        '6': ('Bidirectional', gui.bidirectional)
    }
    
    if choice in algorithms:
        name, func = algorithms[choice]
        gui.ax.set_title(f"Running {name}...")
        path = func()
        if path:
            gui.ax.set_title(f"{name} Found Path!")
            gui.update_plot(path=path)
        else:
            gui.ax.set_title("No Path Found")
        plt.show()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()