# Mobile app (Expo)

## Baseline
Expo SDK 57 or newer (SDK 57 shipped in June 2026 on React Native 0.86; SDK 58 targets React Native 0.88 and was in beta in October 2026, so use the newest stable SDK when Phase 3 starts), React Native New Architecture, Hermes, TypeScript strict, Expo Router. Android first; iOS in Phase 5.

## Structure
```
apps/mobile/
  app/               Expo Router routes: (tabs)/feed, search, tracker, resume, profile; job/[id]; auth; settings
  src/components/    components built on the shared tokens
  src/glass/         Skia glass materials, the match orb, shaders
  src/motion/        Reanimated presets, gesture handlers, haptics map
  src/data/          API client, TanStack Query, offline persistence
  app.config.ts      configuration per environment (development, preview, production)
  eas.json           build profiles
```

## Libraries
| Need | Choice |
|---|---|
| Navigation | Expo Router |
| Server state and offline | TanStack Query with MMKV persistence |
| Local state | Zustand |
| Secure storage | expo-secure-store (tokens) |
| Lists | FlashList |
| Animation and gestures | Reanimated 4, Gesture Handler |
| Glass and custom graphics | React Native Skia runtime shaders; expo-glass-effect `GlassView` on iOS 26+ (it renders a plain view elsewhere, so we supply our own fallback) |
| Images | expo-image |
| Push | expo-notifications (FCM on Android, APNs on iOS) |
| Haptics | expo-haptics |
| Designed micro-animations | Rive, where a designed animation beats code |
| Errors | Sentry |

## Liquid Glass on each platform
- **Android:** a Skia runtime shader that blurs, refracts and adds a specular rim over a snapshot of the content behind the surface, used for the tab bar, sheets, the match orb and hero cards. Ordinary cards use a cheaper blur; low-end devices get the solid material. SplitIT already draws its glass with Skia, so reuse what works (Phase 0 archaeology).
- **iOS 26+:** native Liquid Glass through expo-glass-effect for system-like surfaces; Skia for custom ones such as the orb.
- **Accessibility:** "reduce transparency" switches to solid materials; contrast stays at AA.

## Auth
Native Google sign-in returns an ID token; the API verifies it and issues a 15-minute access token and a rotating, device-bound refresh token, both kept in secure storage. Email one-time codes as the fallback; Sign in with Apple joins in Phase 5.

## Offline and sync
The last feed pages, saved jobs and the tracker persist locally; tracker edits queue offline and sync later (last writer wins per field, by server timestamp); a banner shows the offline state.

## Push and deep links
Alerts arrive as push notifications that deep-link to `https://<domain>/job/<id>`; Android App Links are verified through `/.well-known/assetlinks.json` on our domain. Notification permission is requested at a meaningful moment (after the first saved search), never on first launch.

## Performance budgets
| Metric | Budget (mid-range Android) |
|---|---|
| Cold start to interactive feed | under 2.5 s |
| Feed scrolling | 60 fps; janky frames under 5% |
| Swipes and sheets | 60 fps on the UI thread |
| Universal APK size | under 40 MB (Play's AAB downloads are smaller) |
| Crash-free sessions | at least 99.5% |

Measure on Sayandip's phone with Flashlight or Android Studio's profiler, not only on the emulator. Watch the JS bundle with Expo Atlas.

## Builds and releases
| Profile | Output | Use |
|---|---|---|
| development | development-client APK | daily work on the emulator or phone |
| preview | signed release APK (`buildType: apk`) | direct install for Sayandip and testers |
| production | AAB | Google Play (and an IPA for the App Store in Phase 5) |

- **Local builds first** (no queue, no monthly limit): `npx expo prebuild`, then Gradle with the Android SDK at `C:\Users\Sayan\AppData\Local\Android\Sdk` and JDK 17 from `C:\Java\jdk-17`, set for that command only (never change JAVA_HOME globally; his big-data tools depend on it). `/build-apk` wraps this.
- **EAS cloud builds** when needed (the free plan has a monthly build allowance and a 45-minute limit per build): `eas build --profile preview` or `--profile production`.
- **Signing:** EAS-managed credentials, or an upload keystore Sayandip keeps outside the repo; Google Play App Signing for production.
- **Versioning:** semantic app version; build number incremented automatically.
- **Over-the-air updates:** EAS Update for JavaScript-only fixes, with a runtime-version policy so an update never reaches an incompatible binary.

## Testing
Jest + React Native Testing Library for components and hooks; Maestro flows on the emulator or phone (sign in, feed, save, tracker move, alert deep link), run by `/build-apk`; adb screenshots for design review; a manual pass on Sayandip's phone before each release.

## Google Play requirements (checked Nov 2026)
- New apps and updates must target Android 16 (API level 36) since 31 Aug 2026.
- Personal developer accounts created after 13 Nov 2023 must run a closed test with at least 12 testers opted in for 14 continuous days before getting production access.
- Data safety form, privacy policy URL, in-app account deletion plus a web deletion URL, content rating, target audience 18+, minimal permissions (notifications only).
- Android developer verification: enforced from 30 Sept 2026 in Brazil, Indonesia, Singapore and Thailand, and globally in 2027. Play releases are covered by the verified Play account; adb installs stay allowed for testing; Google also offers a free limited-distribution account for students and hobbyists (up to 20 devices).

## iOS (Phase 5)
EAS builds iOS in the cloud, so no Mac is needed; TestFlight on a borrowed iPhone; Sign in with Apple is required when other third-party sign-in is offered; in-app account deletion; privacy nutrition labels; no tracking, so no tracking prompt.
