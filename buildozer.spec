[app]

# (str) Title of your application
title = Admin Alknas

# (str) Package name
package.name = adminalknas

# (str) Package domain (needed for android/ios packaging)
package.domain = org.alknas

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the source info)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 0.1

# (list) Application requirements
# تمت إزالة pillow لتجنب أخطاء C-Libraries وضبط Kivy و KivyMD
requirements = python3,kivy==2.3.0,kivymd==1.2.0

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen to the user
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (list) The Android archs to build for
# arm64-v8a لمعظم الأجهزة الحديثة ولتسريع وقت البناء للنصف
android.archs = arm64-v8a

# (bool) Android allow backup
android.allow_backup = True

# --------------------------------------------------
# إعدادات Android SDK و NDK المستقرة
# --------------------------------------------------

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use (تثبيت 25b يمنع أخطاء NDK 28)
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# --------------------------------------------------
# إعدادات Buildozer العامة
# --------------------------------------------------
[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
