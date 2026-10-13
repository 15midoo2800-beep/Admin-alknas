import os
import hmac
import hashlib
import base64
import json
from datetime import datetime, timedelta
import urllib.parse
import webbrowser

from kivy.core.text import LabelBase
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

# تسجيل الخط العربي إن وجد
if os.path.exists("font.ttf"):
    LabelBase.register(name="AppFont", fn_regular="font.ttf")
    DEFAULT_FONT = "AppFont"
else:
    DEFAULT_FONT = "Roboto"

KV = '''
<KeygenScreen>:
    name: "keygen"
    canvas.before:
        Color:
            rgba: 0.07, 0.09, 0.13, 1
        Rectangle:
            pos: self.pos
            size: self.size

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True

        BoxLayout:
            orientation: "vertical"
            padding: ["18dp", "24dp", "18dp", "24dp"]
            spacing: "14dp"
            size_hint_y: None
            height: self.minimum_height

            # العنوان والشعار
            MDLabel:
                text: "لوحة إصدار التراخيص"
                font_name: root.app_font
                font_size: "24sp"
                bold: True
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.2, 0.85, 0.55, 1
                size_hint_y: None
                height: "40dp"

            MDLabel:
                text: "توليد مفاتيح تشغيل مشفرة ومحددة المدة"
                font_name: root.app_font
                font_size: "14sp"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.6, 0.65, 0.72, 1
                size_hint_y: None
                height: "22dp"

            # بطاقة إدخال كود جهاز العميل
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "10dp"
                radius: [14, 14, 14, 14]
                elevation: 3
                md_bg_color: 0.12, 0.15, 0.21, 1
                size_hint_y: None
                height: "115dp"

                MDLabel:
                    text: "كود جهاز العميل (Device ID):"
                    font_name: root.app_font
                    font_size: "15sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.85, 0.85, 0.85, 1
                    size_hint_y: None
                    height: "24dp"

                MDTextField:
                    id: client_device_id
                    hint_text: "أدخل كود الجهاز هنا (أو الصقه)"
                    font_name_hint_text: root.app_font
                    font_size: "16sp"
                    mode: "rectangle"
                    line_color_focus: 0.2, 0.85, 0.55, 1
                    hint_text_color_normal: 0.5, 0.55, 0.6, 1
                    text_color_normal: 1, 1, 1, 1

            # بطاقة تحديد مدة الصلاحية بالأيام
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                radius: [14, 14, 14, 14]
                elevation: 3
                md_bg_color: 0.12, 0.15, 0.21, 1
                size_hint_y: None
                height: "175dp"

                MDLabel:
                    text: "مدة التشغيل (عدد الأيام):"
                    font_name: root.app_font
                    font_size: "15sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.85, 0.85, 0.85, 1
                    size_hint_y: None
                    height: "24dp"

                # أزرار اختيار سريع للمدد
                GridLayout:
                    cols: 4
                    spacing: "8dp"
                    size_hint_y: None
                    height: "38dp"

                    MDRaisedButton:
                        text: "7 أيام"
                        font_name: root.app_font
                        font_size: "13sp"
                        md_bg_color: 0.18, 0.24, 0.33, 1
                        on_release: root.set_days(7)

                    MDRaisedButton:
                        text: "30 يوم"
                        font_name: root.app_font
                        font_size: "13sp"
                        md_bg_color: 0.18, 0.24, 0.33, 1
                        on_release: root.set_days(30)

                    MDRaisedButton:
                        text: "90 يوم"
                        font_name: root.app_font
                        font_size: "13sp"
                        md_bg_color: 0.18, 0.24, 0.33, 1
                        on_release: root.set_days(90)

                    MDRaisedButton:
                        text: "365 يوم"
                        font_name: root.app_font
                        font_size: "13sp"
                        md_bg_color: 0.18, 0.24, 0.33, 1
                        on_release: root.set_days(365)

                MDTextField:
                    id: days_input
                    text: "30"
                    hint_text: "أو اكتب عدد الأيام يدوياً"
                    input_filter: "int"
                    font_name_hint_text: root.app_font
                    font_size: "16sp"
                    mode: "rectangle"
                    line_color_focus: 0.2, 0.85, 0.55, 1
                    hint_text_color_normal: 0.5, 0.55, 0.6, 1
                    text_color_normal: 1, 1, 1, 1

            # زر إنشاء المفتاح المشفر
            MDRaisedButton:
                text: "إنشاء كود التفعيل ⚡"
                font_name: root.app_font
                font_size: "17sp"
                bold: True
                size_hint_x: 1
                height: "50dp"
                md_bg_color: 0.15, 0.68, 0.37, 1
                on_release: root.generate_key()

            # بطاقة عرض المفتاح المولد
            MDCard:
                orientation: "vertical"
                padding: "16dp"
                spacing: "10dp"
                radius: [14, 14, 14, 14]
                elevation: 4
                md_bg_color: 0.14, 0.18, 0.26, 1
                size_hint_y: None
                height: "210dp"

                MDLabel:
                    text: "مفتاح التفعيل المولد:"
                    font_name: root.app_font
                    font_size: "15sp"
                    theme_text_color: "Custom"
                    text_color: 0.75, 0.75, 0.75, 1
                    size_hint_y: None
                    height: "24dp"

                MDLabel:
                    id: generated_key_label
                    text: "اضغط على زر الإنشاء لعرض الكود"
                    font_size: "13sp"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.85, 0.55, 1
                    size_hint_y: None
                    height: "50dp"
                    halign: "center"

                MDLabel:
                    id: expiry_info_label
                    text: ""
                    font_name: root.app_font
                    font_size: "13sp"
                    theme_text_color: "Custom"
                    text_color: 0.9, 0.7, 0.2, 1
                    size_hint_y: None
                    height: "22dp"
                    halign: "center"

                BoxLayout:
                    orientation: "horizontal"
                    spacing: "10dp"
                    size_hint_y: None
                    height: "44dp"

                    MDRaisedButton:
                        text: "نسخ المفتاح 📋"
                        font_name: root.app_font
                        font_size: "14sp"
                        bold: True
                        size_hint_x: 0.5
                        md_bg_color: 0.2, 0.6, 0.86, 1
                        on_release: root.copy_generated_key()

                    MDRaisedButton:
                        text: "إرسال للعميل 💬"
                        font_name: root.app_font
                        font_size: "14sp"
                        bold: True
                        size_hint_x: 0.5
                        md_bg_color: 0.25, 0.7, 0.4, 1
                        on_release: root.share_via_whatsapp()
'''

class KeygenScreen(Screen):
    app_font = DEFAULT_FONT
    # هذا المفتاح السري يجب أن يكون متطابقاً في تطبيقك وتطبيق العميل
    SECRET_KEY = b"ALKNAS_SECURE_KEY_2026_PRO"

    def set_days(self, days_count):
        self.ids.days_input.text = str(days_count)

    def generate_key(self):
        device_id = self.ids.client_device_id.text.strip()
        days_str = self.ids.days_input.text.strip()

        if not device_id:
            Snackbar(text="يرجى إدخال كود جهاز العميل أولاً", font_size="15sp").open()
            return

        if not days_str or not days_str.isdigit() or int(days_str) <= 0:
            Snackbar(text="يرجى إدخال عدد أيام صالح", font_size="15sp").open()
            return

        days = int(days_str)
        expiry_date = datetime.now() + timedelta(days=days)
        expiry_str = expiry_date.strftime("%Y-%m-%d")

        # بيانات الحمولة (Payload)
        payload = f"{device_id}|{expiry_str}"

        # توقيع رقمي لمنع التعديل والتلاعب (HMAC SHA256)
        signature = hmac.new(self.SECRET_KEY, payload.encode('utf-8'), hashlib.sha256).hexdigest()[:12]

        # تشفير الكود النهائي في صيغة Base64 سهلة النسخ
        raw_key = f"{payload}|{signature}"
        encoded_key = base64.b64encode(raw_key.encode('utf-8')).decode('utf-8')

        # عرض الكود وتاريخ الانتهاء
        self.ids.generated_key_label.text = encoded_key
        self.ids.expiry_info_label.text = f"صالح لمدة {days} يوم (ينتهي في: {expiry_str})"

        Snackbar(text="تم إنشاء كود التفعيل بنجاح!", font_size="15sp", duration=2).open()

    def copy_generated_key(self):
        key = self.ids.generated_key_label.text.strip()
        if not key or "اضغط" in key:
            Snackbar(text="لا يوجد كود لنسخه بعد", font_size="15sp").open()
            return
        Clipboard.copy(key)
        Snackbar(text="تم نسخ كود التفعيل إلى الحافظة بنجاح!", font_size="15sp", duration=2).open()

    def share_via_whatsapp(self):
        key = self.ids.generated_key_label.text.strip()
        info = self.ids.expiry_info_label.text.strip()
        if not key or "اضغط" in key:
            Snackbar(text="قم بإنشاء الكود أولاً قبل الإرسال", font_size="15sp").open()
            return

        message = (
            f"مرحباً بك، إليك كود تفعيل التطبيق الخاص بك:\n\n"
            f"🔑 الكود:\n{key}\n\n"
            f"📅 {info}\n"
            f"يرجى لصق الكود في خانة التفعيل داخل التطبيق."
        )

        encoded_msg = urllib.parse.quote(message)
        url = f"https://api.whatsapp.com/send?text={encoded_msg}"

        if platform == "android":
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(url))
                PythonActivity.mActivity.startActivity(intent)
                return
            except Exception:
                pass

        webbrowser.open(url)


class KeygenApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_string(KV)
        return KeygenScreen()


if __name__ == "__main__":
    KeygenApp().run()
