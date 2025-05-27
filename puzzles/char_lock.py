from puzzle import Puzzle, Puzzle_type
import tkinter as tk
from tkinter import messagebox

class CharLock(Puzzle):
    def __init__(self, name, code, num_chars, title):
        self.p_type = Puzzle_type.CHAR_LOCK
        self.name = name
        self.code = code
        self.num_chars = num_chars
        self.title = title
        self.solved = False

    def display(self):
        self._main_window()
        return self.solved

    def _main_window(self):
        def get_password():
            password = ''.join(spin.get() for spin in spinboxes)
            messagebox.showinfo("Character Lock Value", f"“The character lock is currently showing {password}.”")
            if password == self.code:
                unlock()
            else:
                cancel()

        def cancel():
            root.destroy()
            self.solved = False

        def unlock():
            root.destroy()
            self.solved = True

        # Assert char-only-string as code, cast to uppercase
        assert isinstance(self.code, str), "Expected a string"
        assert self.code.isalpha(), "Expected only characters"
        self.code = self.code.upper()
        self.code = self.code[:self.num_chars]

        # Create Main Window
        root = tk.Tk()
        root.title(self.title)

        # Create Digits (Spinboxes)
        spinboxes = []
        for i in range(self.num_chars):
            spin = tk.Spinbox(root, values=[chr(i) for i in range(65, 91)], width=2, font=("Helvetica", 24), justify='center')
            spin.grid(row=0, column=i, padx=5, pady=10)
            spinboxes.append(spin)

        # Buttons
        btn_confirm = tk.Button(root, text="Confirm", command=get_password, font=("Helvetica", 16))
        btn_confirm.grid(row=1, column=0, columnspan=self.num_chars//2, pady=10)

        btn_cancel = tk.Button(root, text="Cancel", command=cancel, font=("Helvetica", 16))
        btn_cancel.grid(row=1, column=self.num_chars//2, columnspan=self.num_chars//2, pady=10)

        root.mainloop()

# Test
if __name__ == "__main__":
    test_lock = CharLock(name="test", code="LOVE", num_chars=4, title="Test Lock")
    result = test_lock.display()
    print(result)
