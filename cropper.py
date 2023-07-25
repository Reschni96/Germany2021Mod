import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class ImageCropper:
    def __init__(self, master):
        self.master = master
        self.image_path = ''
        self.image = None
        self.tk_image = None
        self.rect_id = None
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()

        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        open_button = tk.Button(button_frame, text='Open Image', command=self.open_image)
        open_button.pack(side=tk.LEFT)

        crop_button = tk.Button(button_frame, text='Crop Image', command=self.crop_image)
        crop_button.pack(side=tk.LEFT)

        save_button = tk.Button(button_frame, text='Save Image', command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_move)

    def open_image(self):
        self.image_path = filedialog.askopenfilename()
        self.image = Image.open(self.image_path)
        self.display_image()

    def display_image(self):
        max_size = (800, 800)
        self.image.thumbnail(max_size)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)

        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_button_move(self, event):
        self.end_x = event.x
        rect_height = 0.75 * (self.end_x - self.start_x)
        self.end_y = self.start_y + rect_height

        self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.end_x, self.end_y)

    def crop_image(self):
        if self.rect_id is not None:
            bbox = self.canvas.coords(self.rect_id)
            if len(bbox) == 4:
                x1, y1, x2, y2 = map(int, bbox)
                if x1 < x2 and y1 < y2:
                    self.image = self.image.crop((x1, y1, x2, y2))
                    self.display_image()

    def save_image(self):
        if self.image is not None:
            base_name, ext = os.path.splitext(self.image_path)
            directory = os.path.dirname(base_name)
            cropped_directory = os.path.join(directory, 'Cropped')

            if not os.path.exists(cropped_directory):
                os.makedirs(cropped_directory)

            new_base_name = os.path.basename(base_name)
            new_image_path = os.path.join(cropped_directory, f"{new_base_name}_cropped{ext}")
            self.image.save(new_image_path)


if __name__ == "__main__":
    root = tk.Tk()
    ImageCropper(root)
    root.mainloop()
