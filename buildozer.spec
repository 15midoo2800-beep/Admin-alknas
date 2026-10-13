[app]
title = Admin Alknas
package.name = adminalknas
package.domain = org.alknas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.1

# نكتب python3 بدون أرقام إصدارات لتقرأها وصفة p4a المستقرة
requirements = python3,kivy==2.3.0,kivymd==1.2.0

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a
android.allow_backup = True

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
