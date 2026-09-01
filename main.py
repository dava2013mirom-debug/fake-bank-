import json
import os
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty

KV = """
#:import dp kivy.metrics.dp

<BankScreen>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.08, 0.09, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Верхний бар
    BoxLayout:
        size_hint_y: None
        height: dp(56)
        padding: [dp(20), dp(10)]
        Label:
            text: "FakeBank Mobile"
            font_size: '20sp'
            bold: True
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            color: 1, 1, 1, 1

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True

        BoxLayout:
            orientation: 'vertical'
            padding: [dp(20), dp(10)]
            spacing: dp(16)
            size_hint_y: None
            height: self.minimum_height

            # Карточка счета
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(170)
                padding: dp(16)
                spacing: dp(10)
                canvas.before:
                    Color:
                        rgba: 0.16, 0.22, 0.35, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(16)]

                Label:
                    text: "Текущий счет"
                    font_size: '14sp'
                    color: 0.7, 0.75, 0.85, 1
                    size_hint_y: None
                    height: dp(20)
                    halign: 'left'
                    text_size: self.size

                Label:
                    text: root.balance_str
                    font_size: '28sp'
                    bold: True
                    color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(40)
                    halign: 'left'
                    text_size: self.size

                Widget:

                BoxLayout:
                    size_hint_y: None
                    height: dp(24)
                    Label:
                        text: "•••• 8824"
                        font_size: '15sp'
                        color: 0.8, 0.85, 0.9, 1
                        halign: 'left'
                        text_size: self.size
                    Label:
                        text: "VALID 12/28"
                        font_size: '12sp'
                        color: 0.6, 0.65, 0.75, 1
                        halign: 'right'
                        text_size: self.size

            # Блок перевода / списания
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(190)
                padding: dp(16)
                spacing: dp(10)
                canvas.before:
                    Color:
                        rgba: 0.12, 0.14, 0.18, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(14)]

                Label:
                    text: "Быстрый перевод"
                    font_size: '16sp'
                    bold: True
                    color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(22)
                    halign: 'left'
                    text_size: self.size

                TextInput:
                    id: target_card
                    hint_text: "Номер карты или телефона получателя"
                    multiline: False
                    size_hint_y: None
                    height: dp(42)
                    background_color: 0.18, 0.20, 0.25, 1
                    foreground_color: 1, 1, 1, 1
                    cursor_color: 1, 1, 1, 1
                    padding: [dp(10), dp(10)]

                TextInput:
                    id: transfer_amount
                    hint_text: "Сумма (₽)"
                    input_filter: 'float'
                    multiline: False
                    size_hint_y: None
                    height: dp(42)
                    background_color: 0.18, 0.20, 0.25, 1
                    foreground_color: 1, 1, 1, 1
                    cursor_color: 1, 1, 1, 1
                    padding: [dp(10), dp(10)]

                BoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)

                    Button:
                        text: "Перевести"
                        background_normal: ''
                        background_color: 0.22, 0.53, 0.95, 1
                        bold: True
                        on_release: root.process_transfer()

                    Button:
                        text: "+1 000 ₽"
                        size_hint_x: 0.4
                        background_normal: ''
                        background_color: 0.18, 0.65, 0.38, 1
                        on_release: root.add_funds(1000)

            # Статусное сообщение
            Label:
                text: root.status_msg
                font_size: '14sp'
                color: root.status_color
                size_hint_y: None
                height: dp(24)

            # Заголовок истории
            Label:
                text: "История операций"
                font_size: '16sp'
                bold: True
                color: 0.9, 0.9, 0.9, 1
                size_hint_y: None
                height: dp(24)
                halign: 'left'
                text_size: self.size

            # Контейнер для строк истории
            BoxLayout:
                id: history_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)
"""

class BankScreen(BoxLayout):
    balance = NumericProperty(50000.0)
    balance_str = StringProperty("50 000.00 ₽")
    status_msg = StringProperty("")
    status_color = ListProperty([0.8, 0.8, 0.8, 1])

    def __init__(self, storage_path, **kwargs):
        super().__init__(**kwargs)
        self.storage_file = storage_path
        self.history_items = []
        self.load_state()
        self.render_history()

    def update_balance_display(self):
        self.balance_str = f"{self.balance:,.2f} ₽".replace(",", " ")

    def load_state(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.balance = float(data.get("balance", 50000.0))
                    self.history_items = data.get("history", [])
            except Exception:
                self.balance = 50000.0
                self.history_items = []
        else:
            self.history_items = [
                {"title": "Бонус за открытие карты", "amount": "+50 000.00 ₽", "time": datetime.now().strftime("%d.%m %H:%M"), "type": "in"}
            ]
            self.save_state()
        self.update_balance_display()

    def save_state(self):
        data = {
            "balance": self.balance,
            "history": self.history_items
        }
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def render_history(self):
        container = self.ids.history_container
        container.clear_widgets()

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.metrics import dp

        for item in reversed(self.history_items[-10:]):
            row = BoxLayout(size_hint_y=None, height=dp(48), padding=[dp(12), dp(6)])
            
            left = BoxLayout(orientation='vertical')
            t_lbl = Label(text=item.get("title", ""), font_size='14sp', color=(1, 1, 1, 1), halign='left', text_size=(dp(200), None))
            d_lbl = Label(text=item.get("time", ""), font_size='11sp', color=(0.5, 0.5, 0.6, 1), halign='left', text_size=(dp(200), None))
            left.add_widget(t_lbl)
            left.add_widget(d_lbl)

            is_in = item.get("type") == "in"
            amt_col = (0.2, 0.8, 0.4, 1) if is_in else (0.9, 0.3, 0.3, 1)
            a_lbl = Label(text=item.get("amount", ""), font_size='15sp', bold=True, color=amt_col, halign='right', text_size=(dp(120), None))

            row.add_widget(left)
            row.add_widget(a_lbl)
            container.add_widget(row)

    def process_transfer(self):
        raw_val = self.ids.transfer_amount.text.strip()
        recipient = self.ids.target_card.text.strip()

        if not recipient:
            self.show_status("Введите получателя", (0.9, 0.3, 0.3, 1))
            return
        if not raw_val:
            self.show_status("Введите сумму перевода", (0.9, 0.3, 0.3, 1))
            return

        try:
            val = float(raw_val)
        except ValueError:
            self.show_status("Неверный формат суммы", (0.9, 0.3, 0.3, 1))
            return

        if val <= 0:
            self.show_status("Сумма должна быть больше 0", (0.9, 0.3, 0.3, 1))
            return

        if val > self.balance:
            self.show_status("Недостаточно средств", (0.9, 0.3, 0.3, 1))
            return

        self.balance -= val
        self.update_balance_display()

        self.history_items.append({
            "title": f"Перевод ({recipient})",
            "amount": f"-{val:,.2f} ₽".replace(",", " "),
            "time": datetime.now().strftime("%d.%m %H:%M"),
            "type": "out"
        })
        self.save_state()
        self.render_history()

        self.ids.transfer_amount.text = ""
        self.ids.target_card.text = ""
        self.show_status(f"Списано: {val:,.2f} ₽", (0.2, 0.8, 0.4, 1))

    def add_funds(self, amount):
        self.balance += amount
        self.update_balance_display()
        self.history_items.append({
            "title": "Пополнение баланса",
            "amount": f"+{amount:,.2f} ₽".replace(",", " "),
            "time": datetime.now().strftime("%d.%m %H:%M"),
            "type": "in"
        })
        self.save_state()
        self.render_history()
        self.show_status(f"Начислено: {amount} ₽", (0.2, 0.8, 0.4, 1))

    def show_status(self, text, color):
        self.status_msg = text
        self.status_color = color


class FakeBankApp(App):
    def build(self):
        Builder.load_string(KV)
        storage = os.path.join(self.user_data_dir, "fake_bank.json")
        return BankScreen(storage_path=storage)


if __name__ == "__main__":
    FakeBankApp().run()
  
