from independent_puzzle import IndependentPuzzle, Indep_puzzle_type
import tkinter as tk

class PureLogic(IndependentPuzzle):
    """
    code: hint only
    """
    def __init__(self, name, riddle, code, title=""):
        self.p_type = Indep_puzzle_type.PURE_LOGIC
        self.name = name
        self.code = code
        self.riddle = riddle
        self.title = title
        if not title:
            self.title = name
        self.displayed = False

    def display(self):
        self._main_window()
        self.displayed = True
        return self.displayed
    
    def _main_window(self):
        def cancel():
            msg.destroy()
            root.destroy()

        def show_custom_message():
            msg.configure(bg='black')
            msg.title(self.title)
            msg.geometry("300x100")

            label = tk.Label(msg, text=self.riddle, fg="white", bg="black", font=("Helvetica", 12))
            label.pack(pady=20)

            btn = tk.Button(msg, text="Close", command=cancel, bg="gray", fg="white")
            btn.pack()

        root = tk.Tk()
        root.withdraw()  # Hide main window
        msg = tk.Toplevel()

        show_custom_message()
        root.mainloop()

# Test
if __name__ == "__main__":
    test_logic = PureLogic(name="test", riddle="1 + 2", code="3", title="Test Lock")
    result = test_logic.display()
    print(result)
