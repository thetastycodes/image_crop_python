import os
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class Cropers(Tk):
    # Digunakan untuk lebar dan tinggi 
    # dari window & canvas
    WIDTH = 300
    HEIGHT = 100
    CURSOR = 'cross'
    CROP_MODE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(".:: Cropers ::.")
        self.geometry(f'{Cropers.WIDTH}x{Cropers.HEIGHT}')
        
        self.menu = None
        self.create_menu()

        self.canvas = None
        self.draw_canvas()

        self.image = None
        self.photo_image = None
        self.canvas_image = None

        self.x1 = None
        self.y1 = None
        self.rectangle = None

    def create_menu(self):
        self.menu = Menu(self)
        self.menu.add_command(label="Open Image", command=self.choose_image)
        self.config(menu=self.menu)

    def draw_canvas(self):
        self.canvas = Canvas(
            self,
            width=Cropers.WIDTH,
            height=Cropers.HEIGHT,
            cursor=Cropers.CURSOR,
        )
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def choose_image(self):
        filetypes = (
            ('Image PNG', '*.png'),
            ('Image JPG', '*.jpg'),
            ('Image JPEG', '*.jpeg'),
        )
        filename = filedialog.askopenfile(
            title="Open file",
            initialdir='/',
            filetypes=filetypes
        )

        self.image = Image.open(filename.name)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas_image = self.canvas.create_image(
            0, 0,
            anchor=NW,
            image=self.photo_image
        )

        new_width, new_height = self.image.size
        self.canvas.configure(
            width=new_width,
            height=new_height
        )
        self.geometry(f'{new_width}x{new_height}')
        Cropers.CROP_MODE = True

    def on_press(self, event):
        if Cropers.CROP_MODE:
            # Remove rectangle exists
            self.canvas.delete(self.rectangle)

            # Get and save mouse drag start position
            self.x1 = event.x
            self.y1 = event.y

            # Create new rectangle
            self.rectangle = self.canvas.create_rectangle(
                self.x1,
                self.y1,
                1, 1,
                outline='blue'
            )
    
    def on_move(self, event):
        if Cropers.CROP_MODE:
            current_x, current_y = event.x, event.y
            # Expanding rectangle when you drag using mouse
            self.canvas.coords(
                self.rectangle,
                self.x1,
                self.y1,
                current_x,
                current_y
            )

    def clear(self):
        self.canvas.delete(self.canvas_image)
        self.canvas.configure(width=Cropers.WIDTH, height=Cropers.HEIGHT)
        self.geometry(f'{Cropers.WIDTH}x{Cropers.HEIGHT}')
        self.canvas.delete(self.rectangle)
        Cropers.CROP_MODE = False

    def on_release(self, event):
        if Cropers.CROP_MODE:
            crop_image = self.image.crop(self.canvas.bbox(self.rectangle))
            head, name = os.path.split(self.image.filename)
            datetime_name = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            name = f'crop_{datetime_name}_{name}'
            directory = filedialog.askdirectory()

            if directory:
                crop_image.save(os.path.join(directory, name))
                crop_image.show()
                # Remove image from canvas
                self.clear()

if __name__ == '__main__':
    app = Cropers()
    app.mainloop()