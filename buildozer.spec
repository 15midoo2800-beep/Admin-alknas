[app]
title = Admin Alknas
package.name = adminalknas
package.domain = org.alknas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow
orientation = portrait
osx.kivy_version = 2.3.0
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a
android.allow_backup = True

# تثبيت إصدارات NDK و SDK المستقرة وتجنب NDK 28
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
