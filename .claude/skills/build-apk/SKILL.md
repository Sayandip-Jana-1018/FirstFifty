---
name: build-apk
description: Build FirstFifty's Android app (debug build, preview APK or production AAB), install it on the emulator or Sayandip's phone with adb, run the Maestro smoke flow, and capture screenshots and cold-start time. Use whenever an Android build is needed or a mobile change must be checked on a device.
argument-hint: "[debug|preview|production] [local|eas]"
---

Profile and method: $ARGUMENTS (default: preview, local).

Paths on this PC: Android SDK `C:\Users\Sayan\AppData\Local\Android\Sdk` (adb at `platform-tools\adb.exe`, the emulator at `emulator\emulator.exe`); JDK 17 at `C:\Java\jdk-17`.

1. **Device:** `adb devices`. If none, list emulators (`emulator -list-avds`) and start one (`emulator -avd <name> -no-snapshot-save`), or ask Sayandip to plug in his phone with USB debugging on. If no emulator exists, ask him to create one (docs/SETUP.md item 4).
2. **Build locally:** in `apps/mobile`, `npx expo prebuild --platform android` (the generated folder is gitignored); then, with `JAVA_HOME` set to JDK 17 and `ANDROID_HOME` to the SDK for that command only (in Git Bash, `JAVA_HOME=/c/Java/jdk-17 ANDROID_HOME=/c/Users/Sayan/AppData/Local/Android/Sdk ./gradlew ...`; never change them globally), run the Gradle wrapper in `android/`: `assembleRelease` for an APK or `bundleRelease` for an AAB. Signing uses the upload keystore Sayandip keeps outside the repo, or EAS-managed credentials. **With EAS instead:** `npx eas-cli build --platform android --profile <profile>` (uses the monthly free allowance; Sayandip must be signed in to Expo).
3. **Install and smoke-test:** `adb install -r <apk>`, launch the app, and run `maestro test .maestro/smoke.yaml` if Maestro is installed; otherwise do a scripted tap-through with adb and say so.
4. **Screenshots:** `adb exec-out screencap -p > docs/design/reviews/<date>-android/<screen>.png` for the key screens.
5. **Cold start:** `adb shell am start -W <package>/<activity>` and report TotalTime; note any jank you see.
6. **Report:** APK or AAB path and size, device, smoke result, cold-start time, screenshots, issues. Copy a preview APK into `dist/` (gitignored) and tell Sayandip how to install it on his phone.
