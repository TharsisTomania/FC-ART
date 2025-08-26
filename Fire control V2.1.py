import tkinter as tk
from tkinter import messagebox
import math

class SquareMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Map Application")
        
        # Set fixed window size
        self.root.geometry("720x560")
        self.root.resizable(False, False)  # Prevent resizing

        # Input fields
        tk.Label(root, text="Square Size (meters):").pack()
        self.square_size_entry = tk.Entry(root)
        self.square_size_entry.pack()

        tk.Label(root, text="Number of Squares (per side):").pack()
        self.num_squares_entry = tk.Entry(root)
        self.num_squares_entry.pack()

        tk.Button(root, text="Draw Map", command=self.draw_map).pack()

        # Canvas
        self.canvas = tk.Canvas(root, bg="white", width=720, height=560)
        self.canvas.pack(expand=True, fill="both")

        # Variables for clicks
        self.pointA = None
        self.pointB = None

        # Result and Clear button container
        self.result_frame = tk.Frame(root)
        self.result_frame.pack()

    def draw_map(self):
        try:
            self.square_size = float(self.square_size_entry.get())  # in meters
            self.num_squares = int(self.num_squares_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        # Calculate the maximum number of squares that fit into the window
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Check if the grid fits within the window dimensions
        total_width = self.square_size * self.num_squares
        total_height = self.square_size * self.num_squares

        # If the total width/height exceeds the window size, calculate the zoom factor
        zoom_factor = min(canvas_width / total_width, canvas_height / total_height)

        # Adjust the square size based on the zoom factor
        self.adjusted_square_size = self.square_size * zoom_factor

        # If the zoom_factor is less than 1, scale down the grid
        if zoom_factor < 1:
            print(f"Zooming down: New adjusted square size = {self.adjusted_square_size:.2f} meters")

        self.canvas.delete("all")  # Clear before redrawing
        self.canvas.config(width=canvas_width, height=canvas_height)

        # Draw grid with the adjusted square size
        for i in range(self.num_squares + 1):
            # vertical lines
            self.canvas.create_line(i * self.adjusted_square_size, 0,
                                    i * self.adjusted_square_size, canvas_height)
            # horizontal lines
            self.canvas.create_line(0, i * self.adjusted_square_size,
                                    canvas_width, i * self.adjusted_square_size)

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
            # Calculate pixel distance between points
            dx_pixels = self.pointB[0] - self.pointA[0]
            dy_pixels = self.pointB[1] - self.pointA[1]
            pixel_distance = math.sqrt(dx_pixels ** 2 + dy_pixels ** 2)

            # Convert pixel distance to meters
            distance_in_meters = pixel_distance * (self.square_size / self.adjusted_square_size)

            # Show result
            self.show_result(distance_in_meters)

    def show_result(self, distance_in_meters):
        # Display distance in meters
        messagebox.showinfo("Distance", f"Distance between A and B: {distance_in_meters:.2f} meters")

        # Remove any previous buttons and show the "Clear" button
        for widget in self.result_frame.winfo_children():
            widget.destroy()  # Clear previous content

        # Add Clear button
        tk.Button(self.result_frame, text="Clear", command=self.clear).pack()

    def clear(self):
        # Reset points
        self.pointA = None
        self.pointB = None

        # Clear canvas
        self.canvas.delete("all")

        # Reset input fields
        self.square_size_entry.delete(0, tk.END)
        self.num_squares_entry.delete(0, tk.END)

        # Redraw grid if needed (for when we want to draw it again)
        self.canvas.config(width=720, height=560)

        # Hide the Clear button after reset
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Optionally, focus back to input fields
        self.square_size_entry.focus()

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = SquareMapApp(root)
    root.mainloop()
