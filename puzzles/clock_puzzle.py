from puzzle import Puzzle, Puzzle_type
import tkinter as tk
import math

class ClockPuzzle(Puzzle):
    """
    p_type: the type of the puzzle
    name: the name of the puzzle
    target_hour: an int, ranging from 0-11
    target_minute: an int, ranging from 0-59
    title: the title of the window
    solved: return whether the puzzle is solved
    hour_angle: the hour hand's angle on the clock, ranging from 0-360
    minute_angle: the minute hand's angle on the clock, ranging from 0-360
    """
    def __init__(self, name, target_hour, target_minute, title):
        self.p_type = Puzzle_type.CLOCK_PUZZLE
        self.name = name
        self.target_hour = target_hour
        self.target_minute = target_minute
        self.title = title
        self.solved = False
        assert 0 <= self.target_hour < 12, "Set hour not valid!"
        assert 0 <= self.target_minute < 60, "Set minute not valid!"
        self.hour_angle = 300     # Initial time: 10:10
        self.minute_angle = 60   

    def display(self):
        self._main_window()
        return self.solved
    
    def _main_window(self):
        def cancel():
            self.root.destroy()
            self.solved = False

        self.root = tk.Tk()
        self.root.title(self.title)
        self.canvas_size = 400
        self.canvas_extra_height = 100
        self.center = self.canvas_size // 2
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size + self.canvas_extra_height, bg="white")
        self.canvas.pack()

        self.hour_angle = 300     # 0 ~ 360
        self.minute_angle = 60   # 0 ~ 360
        self.dragging_hand = None  # 'hour' or 'minute'

        self._draw_clock()
        self._draw_hands()

        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._do_drag)
        self.canvas.bind("<ButtonRelease-1>", self._end_drag)

        btn_cancel = tk.Button(self.root, text="Cancel", command=cancel, font=("Helvetica", 16))
        self.canvas.create_window(self.center, self.canvas_size + self.canvas_extra_height//2, window=btn_cancel)

        self.root.mainloop()

    def _draw_clock(self):
        self.canvas.create_oval(50, 50, 350, 350, outline="black", width=3)
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            x1 = self.center + 140 * math.sin(rad)
            y1 = self.center - 140 * math.cos(rad)
            x2 = self.center + 160 * math.sin(rad)
            y2 = self.center - 160 * math.cos(rad)
            self.canvas.create_line(x1, y1, x2, y2, width=2)
    
    def _draw_hands(self):
        self.canvas.delete("hands")
        # Minute Hand
        rad_minute = math.radians(self.minute_angle)
        x_minute = self.center + 120 * math.sin(rad_minute)
        y_minute = self.center - 120 * math.cos(rad_minute)
        self.canvas.create_line(self.center, self.center, x_minute, y_minute, fill="blue", width=3, tag="hands")
        # Hour Hand
        rad_hour = math.radians(self.hour_angle)
        x_hour = self.center + 80 * math.sin(rad_hour)
        y_hour = self.center - 80 * math.cos(rad_hour)
        self.canvas.create_line(self.center, self.center, x_hour, y_hour, fill="red", width=5, tag="hands")

    def _angle_from_mouse(self, event):
        dx = event.x - self.center
        dy = self.center - event.y
        angle = math.degrees(math.atan2(dx, dy)) % 360
        return angle
    
    def _start_drag(self, event):
        angle = self._angle_from_mouse(event)
        # Determine which hand is being dragged 
        hour_diff = abs(angle - self.hour_angle) % 360
        minute_diff = abs(angle - self.minute_angle) % 360
        if minute_diff < hour_diff:
            self.dragging_hand = 'minute'
        else:
            self.dragging_hand = 'hour'

    def _do_drag(self, event):
        angle = self._angle_from_mouse(event)
        if self.dragging_hand == 'hour':
            # Every hour turns 30°, and then split to 5 parts further
            self.hour_angle = angle // 6 * 6
        elif self.dragging_hand == 'minute':
            # Every minute turns 6°
            self.minute_angle = angle // 6 * 6
        self._draw_hands()

    def _end_drag(self, event):
        self.dragging_hand = None
        self._check_solution()

    def _check_solution(self):
        # Every minute turns 6°
        target_minute_angle = self.target_minute * 6
        # Every hour turns 30°, then every 60/5=12 minutes turn 6° further
        target_hour_angle = self.target_hour * 30 + self.target_minute // 12 * 6
        if self.hour_angle == target_hour_angle and self.minute_angle == target_minute_angle:
            self.root.destroy()
            self.solved = True

# Test
if __name__ == "__main__":
    test_clock = ClockPuzzle(name="test", target_hour=5, target_minute=30, title="Test Clock")
    result = test_clock.display()
    print(result)