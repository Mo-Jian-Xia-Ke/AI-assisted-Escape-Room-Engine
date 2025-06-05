# TODO: UI-Manager
# 创建一个 GUI 控制中心，例如一个 UIManager 类，由主程序负责初始化 GUI
# 其他模块（如 hint 生成器、puzzle 控制器）不要直接创建窗口，而是调用 UIManager 提供的接口显示内容或更新组件

import tkinter as tk
from tkinter import scrolledtext

class WindowDisplay():
    def __init__(self, title="Room Interaction", text=""):
        self.title = title
        self.text = text
        self.root = None
        self.text_area = None
        self.input_box = None
        self.send_button = None

    def display(self):
        self.root_init()
        self.text_area_init()
        self.input_box_init()
        self.send_button = self.button_init("Send", self.handle_input)
        self.root.mainloop()

    def add_text(self, input):
        # Reaction logic
        response = f"\nYou said: {input}"
        self.text += f"> {input}{response}\n"
        
        # Update text
        self.text_area.config(state=tk.NORMAL)
        # 1st row, 0th column
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.text)
        self.text_area.config(state=tk.DISABLED)

    def destroy(self):
        self.root.destroy()

    def handle_input(self):
        user_input = self.input_box.get()
        self.input_box.delete(0, tk.END)

        return user_input
        # Reaction logic
        response = f"\nYou said: {user_input}"
        room_text = f"> {user_input}{response}\n"
        
        # Update text
        self.text_area.config(state=tk.NORMAL)
        # 1st row, 0th column
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, room_text)
        self.text_area.config(state=tk.DISABLED)

    # Create a main window
    def root_init(self):
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.configure(bg="black")
        self.root.geometry("600x400")  # width 600，height 400

    # Insert text into the window
    def text_area_init(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=15,
                                        bg="black", fg="white", font=("Courier", 12))
        # text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)  # read_only
        self.text_area.pack(fill=tk.X, padx=10, pady=(10, 5))

    # Add an input box in the window
    def input_box_init(self):
        self.input_box = tk.Entry(self.root, font=("Courier", 12), bg="black", fg="white", insertbackground="white")
        self.input_box.pack(fill=tk.X, padx=10, pady=5)
        self.input_box.bind("<Return>", self.handle_input)

    # Add a button in the window
    def button_init(self, text, command):
        button = tk.Button(self.root, text=text, command=command, bg="#333", fg="white", font=("Courier", 12))
        button.pack(pady=5)
        return button

# Test
def test():
    initial_text = "You are in a dark room. There is a door to the north.\n"
    window = WindowDisplay("Room Interaction", initial_text)
    
    while True:
        text = window.display()
        if text:
            window.add_text(text)
