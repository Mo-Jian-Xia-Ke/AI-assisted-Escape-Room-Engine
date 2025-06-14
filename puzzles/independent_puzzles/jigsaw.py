from .independent_puzzle import IndependentPuzzle, IndepPuzzleType
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class _PuzzlePiece:
    """
        TODO (Not complete yet)
    """
    def __init__(self, jigsaw, canvas, image, target_x, target_y, size, offset_max):
        self.jigsaw = jigsaw
        self.canvas = canvas
        self.image = image
        self.size = size
        self.target_x = target_x
        self.target_y = target_y

        self.offset_x = random.randint(0, offset_max)
        self.offset_y = random.randint(0, offset_max)

        self.id = canvas.create_image(self.offset_x, self.offset_y, image=image, anchor='nw')
        self.canvas.tag_bind(self.id, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.id, dx, dy)
        self.start_x = event.x
        self.start_y = event.y

    def on_release(self, event):
        x, y = self.canvas.coords(self.id)
        if abs(x - self.target_x) < self.size // 4 and abs(y - self.target_y) < self.size // 4:
            self.canvas.coords(self.id, self.target_x, self.target_y)
            self.jigsaw.check_puzzle_complete()

    def is_correct(self):
        eps = 5
        x, y = self.canvas.coords(self.id)
        return abs(x - self.target_x) < eps and abs(y - self.target_y) < eps


class Jigsaw(IndependentPuzzle):
    """
        TODO
    """
    def __init__(self, name, image_path, grid_size=3, puzzle_size=600, patch_size=50, title=""):
        self.p_type = IndepPuzzleType.JIGSAW
        self.name = name
        self.image_path = os.path.abspath(image_path)
        self._valid_image_path(str(self.image_path))
        self.grid_size = grid_size
        self.puzzle_size = puzzle_size
        self.patch_size = patch_size
        self.canva_size = puzzle_size + patch_size * 2
        self.piece_size = puzzle_size // grid_size
        if not title:
            self.title = name
        self.pieces = []
        self.solved = False

    def display(self):
        self._main_window()
        return self.solved
    
    # group assertions that confirm the path to the image is valid
    def _valid_image_path(self, path):
        assert os.path.isfile(path), f"Path does not exist or is not a file: {path}"
        assert path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')), f"File is not a recognized image: {path}"
        try:
            # Check image integrity
            with Image.open(path) as img:
                img.verify()
        except Exception as e:
            raise AssertionError(f"Not a valid image file: {path}\nError: {e}")

    def _main_window(self):
        def cancel():
            self.solved = False
            self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title(self.title)

        # Create a canva of canva_size as background
        self.canvas = tk.Canvas(self.root, width=self.canva_size, height=self.canva_size, bg="grey")
        self.canvas.pack()
        # In the middle, draw a black rectangle of puzzle_size as the puzzzle area
        # Ranging from (patch_size, patch_size) to (puzzle_size + canva_size, puzzle_size + canva_size)
        self.canvas.create_rectangle(self.patch_size, self.patch_size, self.puzzle_size + self.patch_size, self.puzzle_size + self.patch_size, fill="black", outline="black")

        # Load and resize the image
        self.image = Image.open(self.image_path).resize((self.puzzle_size, self.puzzle_size))
        self._load_pieces()

        self.button = tk.Button(self.root, text="Close", command=cancel)
        self.canvas.create_window(self.canva_size // 2, self.puzzle_size + self.patch_size*3//2, window=self.button)
        self.root.mainloop()

    # Load all the pieces of the image
    def _load_pieces(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                left = col * self.piece_size
                upper = row * self.piece_size
                box = (left, upper, left + self.piece_size, upper + self.piece_size)
                piece_img = ImageTk.PhotoImage(self.image.crop(box))

                piece = _PuzzlePiece(
                    self, self.canvas, piece_img,
                    # target_x, target_y: targetting upper-left corner of a piece
                    target_x=left + self.patch_size, 
                    target_y=upper + self.patch_size,
                    size=self.piece_size,
                    offset_max=self.canva_size-self.piece_size
                )
                self.pieces.append(piece)

    def check_puzzle_complete(self):
        if all(piece.is_correct() for piece in self.pieces):
            messagebox.showinfo("Success", "Puzzle complete!")
            self.solved = True
            self.root.destroy()

# Test
def test():
    image_path = os.path.abspath("img/room1.png")
    test_jigsaw = Jigsaw(name="Jigsaw", image_path=image_path)
    result = test_jigsaw.display()
    print(result)

if __name__ == "__main__":
    test()
