import puzzle
import tkinter as tk
from tkinter import messagebox

class Digital_Lock(puzzle.Puzzle):
    def __init__(self, name, code, num_digits, title):
        self.p_type = puzzle.Puzzle_type.DIGITAL_LOCK
        self.name = name
        self.code = code
        self.num_digits = num_digits
        self.title = title
        self.solved = False

    def display(self):
        self.main_window()
        return self.solved

    def main_window(self):
        def get_password():
            password = ''.join(spin.get() for spin in spinboxes)
            messagebox.showinfo("Digital Lock Value", f"“The digital lock is currently showing {password}.”")
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

        # Cast code to string, and up to num_digits digits
        self.code = str(self.code).zfill(self.num_digits)
        self.code = self.code[:self.num_digits]

        # Create Main Window
        root = tk.Tk()
        root.title(self.title)

        # Create Digits (Spinboxes)
        spinboxes = []
        for i in range(self.num_digits):
            spin = tk.Spinbox(root, from_=0, to=9, width=2, font=("Helvetica", 24), justify='center')
            spin.grid(row=0, column=i, padx=5, pady=10)
            spinboxes.append(spin)

        # Buttons
        btn_confirm = tk.Button(root, text="Confirm", command=get_password, font=("Helvetica", 16))
        btn_confirm.grid(row=1, column=0, columnspan=self.num_digits//2, pady=10)

        btn_cancel = tk.Button(root, text="Cancel", command=cancel, font=("Helvetica", 16))
        btn_cancel.grid(row=1, column=self.num_digits//2, columnspan=self.num_digits//2, pady=10)

        root.mainloop()

# test_dlock = Digital_Lock(name="test", code=1234, num_digits=4, title="Test Lock")
# result = test_dlock.display()
# print(result)
