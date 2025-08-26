import tkinter as tk
from tkinter import messagebox
import math

class SquareMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Map Application")

        # Input fields
        tk.Label(root, text="Square Size (meters):").pack()
        self.square_size_entry = tk.Entry(root)
        self.square_size_entry.pack()

        tk.Label(root, text="Number of Squares (per side):").pack()
        self.num_squares_entry = tk.Entry(root)
        self.num_squares_entry.pack()

        tk.Button(root, text="Draw Map", command=self.draw_map).pack()

        # Canvas
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(expand=True, fill="both")

        # Variables for clicks
        self.pointA = None
        self.pointB = None

        # Buttons
        tk.Button(root, text="Clear", command=self.clear).pack()

    def draw_map(self):
        try:
            self.square_size = int(self.square_size_entry.get())
            self.num_squares = int(self.num_squares_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        self.canvas.delete("all")  # Clear before redrawing
        self.canvas.config(width=self.square_size * self.num_squares,
                           height=self.square_size * self.num_squares)

        # Draw grid
        for i in range(self.num_squares + 1):
            # vertical lines
            self.canvas.create_line(i * self.square_size, 0,
                                    i * self.square_size, self.square_size * self.num_squares)
            # horizontal lines
            self.canvas.create_line(0, i * self.square_size,
                                    self.square_size * self.num_squares, i * self.square_size)

        # Bind click event
        self.canvas.bind("<Button-1>", self.set_point)

    def set_point(self, event):
        x = event.x
        y = event.y

        if self.pointA is None:
            self.pointA = (x, y)
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", tags="pointA")
            self.canvas.create_text(x, y-10, text="A", fill="red", tags="pointA")
        elif self.pointB is None:
            self.pointB = (x, y)
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue", tags="pointB")
            self.canvas.create_text(x, y-10, text="B", fill="blue", tags="pointB")
            self.calculate_distance()

    def calculate_distance(self):
        if self.pointA and self.pointB:
            dx = (self.pointB[0] - self.pointA[0]) / self.square_size
            dy = (self.pointB[1] - self.pointA[1]) / self.square_size
            distance = math.sqrt(dx**2 + dy**2) * self.square_size
            messagebox.showinfo("Distance", f"Distance between A and B: {distance:.2f} meters")

    def clear(self):
        self.pointA = None
        self.pointB = None
        self.canvas.delete("all")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = SquareMapApp(root)
    root.mainloop()
