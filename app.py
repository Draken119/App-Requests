from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import requests
import json

class CustomBox(BoxLayout):
    def __init__(self, **kwargs):
        super(CustomBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 20]
        self.spacing = 20

        # Estilizando a interface
        self.input_url = TextInput(
            hint_text='Enter URL...',
            size_hint=(1, None),
            height='40dp',
            multiline=False,
            background_color=(1, 1, 1, 0.8),
            foreground_color=(0, 0, 0, 1),
            font_size='18sp',
            padding_y=[10, 10],
            padding_x=[15, 15]
        )

        self.button = Button(
            text="Fetch Data",
            size_hint=(1, None),
            height='50dp',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.button.bind(on_press=self.make_request)

        # Seção do conteúdo retornado
        self.result_label = Label(
            text="Response:",
            size_hint=(1, None),
            height='30dp',
            font_size='20sp',
            color=(0.2, 0.4, 0.6, 1),
            bold=True
        )

        self.result_text = TextInput(
            readonly=True,
            size_hint=(1, None),
            height='150dp',
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            font_size='16sp',
            padding_y=[10, 10],
            padding_x=[15, 15],
            scroll_y=1
        )

        # Separador customizado (linha)
        self.separator = SeparatorLine(size_hint=(1, None), height='2dp')

        # Seção dos headers
        self.headers_label = Label(
            text="Headers:",
            size_hint=(1, None),
            height='30dp',
            font_size='20sp',
            color=(0.2, 0.4, 0.6, 1),
            bold=True
        )

        self.headers_text = TextInput(
            readonly=True,
            size_hint=(1, 1),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            font_size='16sp',
            padding_y=[10, 10],
            padding_x=[15, 15],
            scroll_y=1
        )

        self.scroll_view_result = ScrollView(size_hint=(1, 0.4))
        self.scroll_view_result.add_widget(self.result_text)

        self.scroll_view_headers = ScrollView(size_hint=(1, 0.4))
        self.scroll_view_headers.add_widget(self.headers_text)

        self.add_widget(self.input_url)
        self.add_widget(self.button)
        self.add_widget(self.result_label)
        self.add_widget(self.scroll_view_result)
        self.add_widget(self.separator)
        self.add_widget(self.headers_label)
        self.add_widget(self.scroll_view_headers)

    def make_request(self, instance):
        url = self.input_url.text
        try:
            response = requests.get(url)
            headers_formatted = '\n'.join([f'{k}: {v}' for k, v in response.headers.items()])
            if response.headers.get('Content-Type', '').startswith('application/json'):
                parsed_json = json.dumps(response.json(), indent=4)
                self.result_text.text = parsed_json
            else:
                self.result_text.text = response.text
            self.headers_text.text = headers_formatted
        except requests.exceptions.RequestException as e:
            self.result_text.text = f"Error: {str(e)}"
            self.headers_text.text = ""

class SeparatorLine(Widget):
    def __init__(self, **kwargs):
        super(SeparatorLine, self).__init__(**kwargs)
        with self.canvas:
            Color(0.2, 0.4, 0.6, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class CustomApp(App):
    def build(self):
        Window.clearcolor = (0.9, 0.9, 0.95, 1)  # Cor de fundo da aplicação
        return CustomBox()

if __name__ == '__main__':
    CustomApp().run()
