# This .spec config file tells Buildozer an app's requirements for being built.
# It largely follows the syntax of an .ini file.

[app]

# (str) Title of your application
title = Credit Book App

# (str) Package name
package.name = creditbookapp

# (str) Package domain (needed for android/ios packaging)
# Sulaiman Shah ka custom domain setup
package.domain = org.salman

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3==3.11, kivy==2.3.0, kivymd==1.2.0, pillow

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions - INTERNET PERMISSION IS NOW ACTIVE!
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use (Sahi jagah par set kar diya hai)
android.ndk = 25b

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
