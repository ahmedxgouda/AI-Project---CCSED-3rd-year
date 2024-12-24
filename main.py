import tkinter as tk
from queue import PriorityQueue

class MazeApp:
    """
    A GUI application for solving a maze using Dijkstra's algorithm.
    Attributes:
        root (tk.Tk): The root window of the application.
        canvas (tk.Canvas): The canvas where the maze is drawn.
        rows (int): The number of rows in the maze grid.
        cols (int): The number of columns in the maze grid.
        cell_size (int): The size of each cell in the grid.
        grid (list): A 2D list representing the maze grid.
        start (tuple): The starting cell of the maze.
        end (tuple): The ending cell of the maze.
        solved (bool): A flag indicating whether the maze has been solved.
        reset_button (tk.Button): The button to reset the maze.
        dijkstra_solve_button (tk.Button): The button to solve the maze using Dijkstra's algorithm.
    """
    
    def __init__(self, root):
        """
        Initializes the MazeApp with the given root window.
        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("Maze Solver- AI HACKERS")
        self.canvas = tk.Canvas(root, width=620, height=670, bg="white")
        self.offset = (10, 20)
        self.canvas.pack()
        self.rows = 20
        self.cols = 20
        self.cell_size = 30
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.end = None
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        self.solved = False
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()
        self.dijkstra_solve_button = tk.Button(root, text="Solve with Dijkstra (Shortest Path)", command=self.dijkstra)
        self.dijkstra_solve_button.pack()
        self.dfs_solve_button = tk.Button(root, text="Solve with DFS (Better Performance)", command=self.dfs)
        self.dfs_solve_button.pack()
        # Put a message under the grid indicating that the start is green, end is red, wall is black, and path is blue
        self.message_position = (310, 640)
        self.canvas.create_text(self.message_position[0], self.message_position[1], text="Click to set the start point.", font=("Helvetica", 10), tags="message")
        

    def draw_grid(self):
        """
        Draws the grid for the maze on the canvas.
        """
        for i in range(self.rows):  # Loop through each row
            for j in range(self.cols):  # Loop through each column
                
                # Calculate the coordinates of the top-left corner of the cell
                x1 = j * self.cell_size + self.offset[0]
                y1 = i * self.cell_size + self.offset[1]
                
                # Calculate the coordinates of the bottom-right corner of the cell
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Draw the rectangle on the canvas
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

    def on_click(self, event):
        """
        Handles the click event on the canvas to set the start, end, and wall cells.
        Args:
        event (tk.Event): The event object containing information about the click event.
        """
        x, y = event.x, event.y
        row, col = (y - self.offset[1]) // self.cell_size, (x - self.offset[0]) // self.cell_size
        # Check if the user clicked outside the grid
        if row >= self.rows or col >= self.cols:
            return
        if row < 0 or col < 0:
            return
        # Check if the maze has already been solved
        if self.solved:
            return
        # Calculate the coordinates of the rectangle
        x1 = col * self.cell_size + self.offset[0]
        y1 = row * self.cell_size + self.offset[1]
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        if not self.start and self.grid[row][col] == 0:
            self.start = (row, col)
            self.grid[row][col] = 1
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline="black", fill="green")
            self.canvas.create_text(x1 + 15, y1 + 15, text="Start", font=("Helvetica", 8))
            self.canvas.delete("message")
            self.canvas.create_text(self.message_position[0], self.message_position[1], text="Click to set the end point.", font=("Helvetica", 10), tags="message")
        elif not self.end and self.grid[row][col] == 0:
            self.end = (row, col)
            self.grid[row][col] = 2
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline="black", fill="red")
            self.canvas.create_text(x1 + 15, y1 + 15, text="End", font=("Helvetica", 8))
            self.canvas.delete("message")
            self.canvas.create_text(self.message_position[0], self.message_position[1], text="Click to draw walls. Then click 'Solve'.", font=("Helvetica", 10), tags="message")
        elif self.grid[row][col] == 0:
            self.grid[row][col] = 3
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline="black", fill="black")


    def dijkstra(self):
        """
        Solves the maze using Dijkstra's algorithm.
        """
        # Check if start or end points are not defined
        if not self.start or not self.end:
            return

        start = self.start
        end = self.end
        pq = PriorityQueue()  # Initialize a priority queue to store nodes to explore
        pq.put((0, start))  # Add the start node with a distance of 0
        distances = {start: 0}  # Dictionary to store the shortest distance to each node
        previous = {start: None}  # Dictionary to store the previous node for each node
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible movement directions (up, down, left, right)

        while not pq.empty():
            current_distance, current_node = pq.get()  # Get the node with the smallest distance
            if current_node == end:
                break  # Stop if we have reached the end node

            for direction in directions:
                neighbor = (current_node[0] + direction[0], current_node[1] + direction[1])  # Calculate neighbor's position
                # Check if the neighbor is within bounds and not a wall (represented by 3)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols and self.grid[neighbor[0]][neighbor[1]] != 3:
                    distance = current_distance + 1  # Calculate the distance to the neighbor
                    # If the neighbor has not been visited or a shorter path is found
                    if neighbor not in distances or distance < distances[neighbor]:
                        distances[neighbor] = distance  # Update the shortest distance to the neighbor
                        previous[neighbor] = current_node  # Update the previous node for the neighbor
                        pq.put((distance, neighbor))  # Add the neighbor to the priority queue

        if end not in previous:
            self.no_path()  # If the end node is not reachable
            return  # End node is not reachable
        self.draw_path(previous, end)  # Draw the path from start to end using the previous nodes
        self.solved = True  # Mark the maze as solved
        self.end_game()  # Display a message indicating that the maze has been solved
        

    def dfs(self):
        """
        Solves the maze using Depth First Search.
        """
        # Check if start or end points are not defined
        if not self.start or not self.end:
            return

        start = self.start
        end = self.end
        stack = [start]
        visited = set()
        previous = {start: None}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while stack:
            current_node = stack.pop()
            if current_node == end:
                break
            visited.add(current_node)
            for direction in directions:
                neighbor = (current_node[0] + direction[0], current_node[1] + direction[1])
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols and self.grid[neighbor[0]][neighbor[1]] != 3:
                    if neighbor not in visited:
                        previous[neighbor] = current_node
                        stack.append(neighbor)
                        
        if end not in previous:
            self.no_path()
            return
        self.draw_path(previous, end)
        self.solved = True
        self.end_game()

    def get_path(self, previous, end):
        """
        Draws the path from the start to the end cell based on the previous nodes.
        Args:
        previous (dict): A dictionary mapping each cell to its previous cell in the path.
        end (tuple): The ending cell of the maze.
        """
        current = end
        path = []
        while current:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path
    
    def draw_path(self, previous, end):
        """
        Draws the path from the start to the end cell based on the previous nodes.
        Args:
        previous (dict): A dictionary mapping each cell to its previous cell in the path.
        end (tuple): The ending cell of the maze.
        """
        self.dfs_solve_button.config(state="disabled")
        self.dijkstra_solve_button.config(state="disabled")
        path = self.get_path(previous, end)
        for cell in path[1:-1]:
            row, col = cell
            x1 = col * self.cell_size + self.offset[0]
            y1 = row * self.cell_size + self.offset[1]
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         outline="black", fill="blue")
            self.root.after(100, self.canvas.update())
    
                
    def no_path(self):
        """
        Displays a message indicating that there is no path from the start to the end.
        """
        self.canvas.create_text(310, 335, text="No path found!", fill="red", font=("Helvetica", 24))
        self.dfs_solve_button.config(state="disabled")
        self.dijkstra_solve_button.config(state="disabled")
        
    def end_game(self):
        """
        Displays a message indicating that the maze has been solved.
        """
        self.canvas.create_text(310, 335, text="Maze solved!", fill="green", font=("Helvetica", 24))
        self.canvas.delete("message")
        self.canvas.create_text(self.message_position[0], self.message_position[1], text="Congratulations!", font=("Helvetica", 12), tags="message", fill="green")
        self.dijkstra_solve_button.config(state="disabled")
        self.dfs_solve_button.config(state="disabled")

    def reset(self):
        """
        Resets the maze to its initial state.
        """
        self.canvas.delete("all")
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = None
        self.end = None
        self.solved = False
        self.dijkstra_solve_button.config(state="normal")
        self.dfs_solve_button.config(state="normal")
        self.draw_grid()
        self.canvas.create_text(self.message_position[0], self.message_position[1], text="Click to set the start point.", font=("Helvetica", 10), tags="message")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()