import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

class PaintApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Paint App")
        self.initialize_canvas()
        self.initialize_toolbar()
        self.bind_events()

    def initialize_canvas(self):
        self.canvas = tk.Label(self.root)
        self.canvas.place(x=0, y=0)
        self.blank_image = 255 * np.ones((600, 800, 3), dtype=np.uint8)
        self.current_image = self.blank_image.copy()
        self.update_canvas(self.current_image)

    def initialize_toolbar(self):
        self.toolbar = tk.Frame(self.root, width=800, height=50, bg="lightgray")
        self.toolbar.place(x=0, y=550)
        self.tools = ['Line', 'Polyline', 'Rectangle', 'Circle', 'Erase']
        for tool in self.tools:
            button = tk.Button(self.toolbar, text=tool, command=lambda t=tool: self.select_tool(t))
            button.pack(side=tk.LEFT, padx=5, pady=5)
        self.brush_size = 2
        self.brush_size_slider = tk.Scale(self.toolbar, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_brush_size)
        self.brush_size_slider.pack(side=tk.LEFT, padx=5, pady=5)
        self.brush_size_slider.set(self.brush_size)

    def bind_events(self):
        self.start_x = self.start_y = 0
        self.drawing = False
        self.selected_tool = None
        self.canvas.bind("<Button-1>", self.on_draw_start)
        self.canvas.bind("<B1-Motion>", self.on_draw_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_draw_end)

    def select_tool(self, tool):
        self.selected_tool = tool

    def on_draw_start(self, event):
        self.drawing = True
        self.start_x, self.start_y = event.x, event.y

    def on_draw_move(self, event):
        if self.drawing and self.selected_tool:
            action = getattr(self, f"draw_{self.selected_tool.lower()}", None)
            if callable(action):
                action(event, update=False)

    def on_draw_end(self, event):
        if self.drawing and self.selected_tool:
            action = getattr(self, f"draw_{self.selected_tool.lower()}", None)
            if callable(action):
                action(event, update=True)
            self.drawing = False

    def draw_line(self, event, update):
        if update:
            cv2.line(self.current_image, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), self.brush_size)
            self.update_canvas(self.current_image)

    def draw_polyline(self, event, update):
        cv2.line(self.current_image, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), self.brush_size)
        if update:
            self.start_x, self.start_y = event.x, event.y
            self.update_canvas(self.current_image)

    def draw_rectangle(self, event, update):
        if update:
            temp_image = self.current_image.copy()
            cv2.rectangle(temp_image, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), self.brush_size)
            self.current_image = temp_image
            self.update_canvas(self.current_image)

    def draw_circle(self, event, update):
        if update:
            radius = int(((self.start_x - event.x) ** 2 + (self.start_y - event.y) ** 2) ** 0.5)
            cv2.circle(self.current_image, (self.start_x, self.start_y), radius, (0, 0, 0), self.brush_size)
            self.update_canvas(self.current_image)

    def erase(self, event, update):
        cv2.circle(self.current_image, (event.x, event.y), self.brush_size, (255, 255, 255), -1)
        self.update_canvas(self.current_image)

    def update_brush_size(self, value):
        self.brush_size = int(value)

    def update_canvas(self, image):
        img_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        self.canvas.config(image=img_tk)
        self.canvas.image = img_tk

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    PaintApp().run()
