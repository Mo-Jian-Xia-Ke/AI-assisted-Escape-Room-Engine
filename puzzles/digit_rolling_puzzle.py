# install kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
from kivy.lang import Builder

kv = '''
<DigitWheel>:
    orientation: 'vertical'
    RecycleView:
        id: rv
        viewclass: 'DigitLabel'
        scroll_type: ['bars', 'content']
        bar_width: 0
        do_scroll_x: False
        RecycleBoxLayout:
            default_size: None, 60
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

<PasswordInput>:
    orientation: 'vertical'
    BoxLayout:
        id: wheels
        orientation: 'horizontal'
        size_hint_y: 0.8
    Button:
        text: "Confirm password"
        size_hint_y: 0.2
        font_size: 20
        on_release: root.show_password()
'''

Builder.load_string(kv)

class DigitLabel(RecycleDataViewBehavior, Label):
    pass

class DigitWheel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rv = self.ids.rv
        self.rv.data = [{'text': str(i)} for i in range(10)] * 5  # Repeat to roll

    def get_selected(self):
        scroll_y = self.rv.scroll_y
        total_items = len(self.rv.data)
        index = int((1 - scroll_y) * total_items)
        return self.rv.data[index % 10]['text']

class PasswordInput(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wheels = []
        for _ in range(4):
            wheel = DigitWheel()
            self.ids.wheels.add_widget(wheel)
            self.wheels.append(wheel)

    def show_password(self):
        password = ''.join(w.get_selected() for w in self.wheels)
        popup = Popup(title="password",
                      content=Label(text=f"You type: {password}"),
                      size_hint=(0.6, 0.4))
        popup.open()

class PuzzleApp(App):
    def build(self):
        return PasswordInput()

if __name__ == '__main__':
    PuzzleApp().run()
