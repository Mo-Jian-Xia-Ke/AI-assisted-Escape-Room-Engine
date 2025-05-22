import tkinter as tk
from tkinter import scrolledtext

# Initial text
room_text = "You are in a dark room. There is a door to the north.\n"

def handle_input():
    user_input = input_box.get()
    input_box.delete(0, tk.END)

    # Reaction logic
    global room_text
    response = f"\nYou said: {user_input}"
    room_text += f"> {user_input}{response}\n"
    
    # Update text
    text_area.config(state=tk.NORMAL)
    # 1st row, 0th column
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, room_text)
    text_area.config(state=tk.DISABLED)




# Create a main window
def root_init(r_title):
    root = tk.Tk()
    root.title(r_title)
    root.configure(bg="black")
    root.geometry("600x400")  # width 600，height 400
    return root

# Insert text into the window
def text_area_init(root, text):
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15,
                                      bg="black", fg="white", font=("Courier", 12))
    text_area.insert(tk.END, text)
    text_area.config(state=tk.DISABLED)  # read_only
    text_area.pack(fill=tk.X, padx=10, pady=(10, 5))
    return text_area

# Add an input box in the window
def input_box_init(root):
    input_box = tk.Entry(root, font=("Courier", 12), bg="black", fg="white", insertbackground="white")
    input_box.pack(fill=tk.X, padx=10, pady=5)
    return input_box

# Add a button in the window
def button_init(root, text, command):
    button = tk.Button(root, text=text, command=command, bg="#333", fg="white", font=("Courier", 12))
    button.pack(pady=5)
    return button

root = root_init("Room Interaction")
text_area = text_area_init(root, room_text)
input_box = input_box_init(root)
send_button = button_init(root, "Send", handle_input)

root.mainloop()
