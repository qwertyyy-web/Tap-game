[app]
title = Tap Game
package.name = tapgame
package.domain = org.tapgame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3
version = 1.0
requirements = python3,pygame
orientation = portrait
fullscreen = 1

android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
