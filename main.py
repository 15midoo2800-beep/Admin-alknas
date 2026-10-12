import hashlib
import hmac
import urllib.parse
from datetime import datetime, timedelta

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import platform

import os
FONT_PATH = "font.ttf" if os.path.exists("font.ttf") else "Roboto"

def ar(text):
    if not text:
        return ""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

# المفتاح السري نفسه المدمج في تطبيق "القناص"
MASTER_SECRET = b"ALKNAS_TACTICAL_MILITARY_KEY_2026_SECURE"

class AlknasKeygenApp(App):
    def build(self):
        self.selected_days = 30
        self.generated_key = ""

        root = BoxLayout(orientation='vertical', padding=14, spacing=10)

        # 1. العنوان
        header = Label(
            text=ar("لوحة إدارة تراخيص القناص 🛡️"),
            font_name=FONT_PATH,
            font_size='18sp',
            bold=True,
            color=(0.2, 0.9, 0.5, 1),
            size_hint=(1, 0.1)
        )
        root.add_widget(header)

        # 2. إدخال كود جهاز العميل
        root.add_widget(Label(text=ar("كود جهاز العميل (Device ID):"), font_name=FONT_PATH, font_size='13sp', size_hint=(1, 0.06)))
        
        dev_row = BoxLayout(orientation='horizontal', spacing=8, size_hint=(1, 0.11))
        self.inp_dev_id = TextInput(
            hint_text=ar("ألصق كود الجهاز هنا..."),
            font_name=FONT_PATH,
            multiline=False,
            font_size='16sp',
            halign='center',
            background_color=(0.95, 0.95, 0.98, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            size_hint=(0.75, 1)
        )
        dev_row.add_widget(self.inp_dev_id)

        btn_paste = Button(
            text=ar("لصق"),
            font_name=FONT_PATH,
            font_size='14sp',
            background_color=(0.2, 0.4, 0.6, 1),
            size_hint=(0.25, 1)
        )
        btn_paste.bind(on_press=self.paste_from_clipboard)
        dev_row.add_widget(btn_paste)
        root.add_widget(dev_row)

        # 3. اختيار مدة الترخيص
        root.add_widget(Label(text=ar("اختر مدة صلاحية الترخيص:"), font_name=FONT_PATH, font_size='13sp', size_hint=(1, 0.06)))
        
        dur_grid = GridLayout(cols=4, spacing=6, size_hint=(1, 0.11))
        self.btn_30 = Button(text=ar("30 يوم"), font_name=FONT_PATH, background_color=(0.1, 0.6, 0.3, 1))
        self.btn_90 = Button(text=ar("3 أشهر"), font_name=FONT_PATH, background_color=(0.2, 0.25, 0.35, 1))
        self.btn_180 = Button(text=ar("6 أشهر"), font_name=FONT_PATH, background_color=(0.2, 0.25, 0.35, 1))
        self.btn_365 = Button(text=ar("سنة"), font_name=FONT_PATH, background_color=(0.2, 0.25, 0.35, 1))

        self.btn_30.bind(on_press=lambda x: self.set_duration(30, self.btn_30))
        self.btn_90.bind(on_press=lambda x: self.set_duration(90, self.btn_90))
        self.btn_180.bind(on_press=lambda x: self.set_duration(180, self.btn_180))
        self.btn_365.bind(on_press=lambda x: self.set_duration(365, self.btn_365))

        dur_grid.add_widget(self.btn_30)
        dur_grid.add_widget(self.btn_90)
        dur_grid.add_widget(self.btn_180)
        dur_grid.add_widget(self.btn_365)
        root.add_widget(dur_grid)

        # 4. زر التوليد
        btn_gen = Button(
            text=ar("⚡ توليد كود التفعيل ⚡"),
            font_name=FONT_PATH,
            font_size='16sp',
            bold=True,
            background_color=(0.15, 0.5, 0.9, 1),
            size_hint=(1, 0.12)
        )
        btn_gen.bind(on_press=self.generate_key)
        root.add_widget(btn_gen)

        # 5. عرض النتيجة
        self.lbl_result = TextInput(
            text="",
            font_name=FONT_PATH,
            readonly=True,
            multiline=True,
            font_size='15sp',
            halign='center',
            background_color=(0.08, 0.1, 0.14, 1),
            foreground_color=(0.2, 1.0, 0.5, 1),
            size_hint=(1, 0.26)
        )
        root.add_widget(self.lbl_result)

        # 6. أزرار الإجراء السريع (نسخ وإرسال واتساب)
        actions = BoxLayout(orientation='horizontal', spacing=8, size_hint=(1, 0.12))
        
        btn_copy = Button(
            text=ar("📋 نسخ المفتاح"),
            font_name=FONT_PATH,
            font_size='14sp',
            background_color=(0.3, 0.35, 0.45, 1)
        )
        btn_copy.bind(on_press=self.copy_key)
        actions.add_widget(btn_copy)

        btn_send_wa = Button(
            text=ar("📲 إرسال للعميل بالواتساب"),
            font_name=FONT_PATH,
            font_size='14sp',
            bold=True,
            background_color=(0.1, 0.65, 0.35, 1)
        )
        btn_send_wa.bind(on_press=self.send_via_whatsapp)
        actions.add_widget(btn_send_wa)
        root.add_widget(actions)

        return root

    def set_duration(self, days, active_btn):
        self.selected_days = days
        for btn in [self.btn_30, self.btn_90, self.btn_180, self.btn_365]:
            btn.background_color = (0.2, 0.25, 0.35, 1)
        active_btn.background_color = (0.1, 0.6, 0.3, 1)

    def paste_from_clipboard(self, instance):
        clip_txt = Clipboard.paste()
        if clip_txt:
            self.inp_dev_id.text = clip_txt.strip()

    def generate_key(self, instance):
        dev_id = self.inp_dev_id.text.strip()
        if not dev_id:
            self.lbl_result.text = ar("يرجى إدخال أو لصق كود الجهاز أولاً!")
            return

        expiry_date = (datetime.now() + timedelta(days=self.selected_days)).strftime("%Y%m%d")
        payload = f"{dev_id}:{expiry_date}".encode('utf-8')
        sig = hmac.new(MASTER_SECRET, payload, hashlib.sha256).hexdigest()[:12].upper()
        self.generated_key = f"ALK-{expiry_date}-{sig}"

        display_text = (
            f"تم توليد الترخيص بنجاح:\n"
            f"الجهاز: {dev_id}\n"
            f"الصلاحية: {self.selected_days} يوم (حتى {expiry_date})\n\n"
            f"المفتاح: {self.generated_key}"
        )
        self.lbl_result.text = ar(display_text)

    def copy_key(self, instance):
        if self.generated_key:
            Clipboard.copy(self.generated_key)
            self.lbl_result.text = ar(f"تم نسخ المفتاح إلى الحافظة بنجاح!\n\n{self.generated_key}")

    def send_via_whatsapp(self, instance):
        if not self.generated_key:
            return

        msg = (
            f"مرحباً بك، ترخيص تطبيق *القناص PRO* الخاص بك جاهز:\n\n"
            f"🔑 *مفتاح التفعيل:*\n`{self.generated_key}`\n\n"
            f"📅 الصلاحية: {self.selected_days} يوم.\n"
            f"قم بفتح التطبيق ولصق الكود لتفعيله مباشرة."
        )
        encoded = urllib.parse.quote(msg)
        wa_url = f"https://api.whatsapp.com/send?text={encoded}"

        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(wa_url))
                PythonActivity.mActivity.startActivity(intent)
                return
            except Exception:
                pass

        import webbrowser
        webbrowser.open(wa_url)

if __name__ == '__main__':
    AlknasKeygenApp().run()
