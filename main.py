import urllib.parse
import uuid
import webbrowser
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

KV = '''
<ActivationScreen>:
    name: "activation"
    canvas.before:
        Color:
            rgba: 0.08, 0.1, 0.14, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: ["20dp", "25dp", "20dp", "25dp"]
        spacing: "16dp"

        # العنوان الرئيسي
        MDLabel:
            text: "تفعيل التطبيق"
            font_name: "font.ttf"
            font_size: "26sp"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            size_hint_y: None
            height: "45dp"

        # بطاقة كود الجهاز
        MDCard:
            orientation: "vertical"
            padding: "16dp"
            spacing: "12dp"
            radius: [16, 16, 16, 16]
            elevation: 4
            md_bg_color: 0.14, 0.17, 0.24, 1
            size_hint_y: None
            height: "135dp"

            MDLabel:
                text: "كود الجهاز الخاص بك:"
                font_name: "font.ttf"
                font_size: "16sp"
                theme_text_color: "Custom"
                text_color: 0.75, 0.75, 0.75, 1
                size_hint_y: None
                height: "25dp"

            BoxLayout:
                orientation: "horizontal"
                spacing: "12dp"

                MDLabel:
                    id: device_id_label
                    text: root.device_id
                    font_size: "20sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.85, 0.55, 1
                    valign: "middle"

                MDRaisedButton:
                    text: "نسخ الكود"
                    font_name: "font.ttf"
                    font_size: "16sp"
                    bold: True
                    md_bg_color: 0.2, 0.6, 0.86, 1
                    on_release: root.copy_device_code()

        # خانة إدخال مفتاح التفعيل
        MDTextField:
            id: key_input
            hint_text: "أدخل كود التفعيل هنا"
            font_name_hint_text: "font.ttf"
            font_size: "18sp"
            mode: "rectangle"
            line_color_focus: 0.2, 0.85, 0.55, 1
            hint_text_color_normal: 0.65, 0.65, 0.65, 1
            text_color_normal: 1, 1, 1, 1

        MDRaisedButton:
            text: "تأكيد التفعيل"
            font_name: "font.ttf"
            font_size: "18sp"
            bold: True
            size_hint_x: 1
            height: "50dp"
            md_bg_color: 0.18, 0.8, 0.44, 1
            on_release: root.verify_license()

        Widget:
            size_hint_y: None
            height: "5dp"

        # بطاقة شراء الاشتراك عبر واتساب
        MDCard:
            orientation: "vertical"
            padding: "16dp"
            spacing: "12dp"
            radius: [16, 16, 16, 16]
            elevation: 3
            md_bg_color: 0.12, 0.15, 0.21, 1
            size_hint_y: None
            height: "170dp"

            MDLabel:
                text: "طلب شراء كود التفعيل:"
                font_name: "font.ttf"
                font_size: "18sp"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: "28dp"

            MDRaisedButton:
                id: duration_btn
                text: "مدة الاشتراك: شهر واحد ▼"
                font_name: "font.ttf"
                font_size: "16sp"
                size_hint_x: 1
                height: "44dp"
                md_bg_color: 0.22, 0.28, 0.38, 1
                on_release: root.open_duration_menu()

            MDRaisedButton:
                text: "إرسال الكود عبر واتساب 💬"
                font_name: "font.ttf"
                font_size: "17sp"
                bold: True
                size_hint_x: 1
                height: "48dp"
                md_bg_color: 0.15, 0.68, 0.37, 1
                on_release: root.send_to_whatsapp()
'''

class ActivationScreen(Screen):
    # رقم الواتساب المباشر
    WHATSAPP_NUMBER = "201155661920"

    def __init__(self, **kwargs):
        # استخراج معرّف فريد للجهاز
        self.device_id = str(uuid.getnode())[:10]
        self.selected_duration = "شهر واحد"
        super().__init__(**kwargs)
        self.menu = None

    def on_kv_post(self, base_widget):
        durations = ["شهر واحد", "3 أشهر", "6 أشهر", "سنة كاملة"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": dur,
                "on_release": lambda x=dur: self.set_duration(x),
            } for dur in durations
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.duration_btn,
            items=menu_items,
            width_mult=4,
        )

    def open_duration_menu(self):
        if self.menu:
            self.menu.open()

    def set_duration(self, text_item):
        self.selected_duration = text_item
        self.ids.duration_btn.text = f"مدة الاشتراك: {text_item} ▼"
        self.menu.dismiss()

    def copy_device_code(self):
        Clipboard.copy(self.device_id)
        Snackbar(
            text="تم نسخ كود الجهاز بنجاح!",
            font_size="16sp",
            duration=2
        ).open()

    def send_to_whatsapp(self):
        message = (
            f"مرحباً، أود شراء تفعيل لتطبيق القناص.\n"
            f"📱 كود جهازي: {self.device_id}\n"
            f"⏳ مدة الاشتراك المطلوبة: {self.selected_duration}"
        )
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{self.WHATSAPP_NUMBER}?text={encoded_message}"
        webbrowser.open(whatsapp_url)

    def verify_license(self):
        entered_key = self.ids.key_input.text.strip()
        if not entered_key:
            Snackbar(text="يرجى إدخال كود التفعيل أولاً").open()
            return

        # مكان دمج منطق التحقق من المفتاح الخاص بك
        Snackbar(text="تم تفعيل التطبيق بنجاح!").open()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_string(KV)
        return ActivationScreen()

if __name__ == "__main__":
    MainApp().run()
