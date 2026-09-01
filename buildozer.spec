[app]
title = FakeBank
package.name = fakebank
package.domain = org.fakebank.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Целевые архитектуры (arm64-v8a подходит для 99% современных смартфонов)
android.archs = arm64-v8a
android.api = 33
android.minapi = 21

# Разрешения
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
