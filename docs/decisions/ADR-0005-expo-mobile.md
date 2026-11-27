# ADR-0005: Expo and React Native for mobile, Android first

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
One TypeScript skill set across web and mobile. Sayandip's SplitIT already ships an Expo app that draws its glass with Skia. React Native's New Architecture performs well, EAS builds iOS without a Mac, and over-the-air updates fix JavaScript bugs without a store release. Most of our users are on Android.

## Decision
Expo (managed workflow with prebuild) for the app, Android first, iOS in Phase 5. React Native Skia for glass and custom graphics on Android; expo-glass-effect for native Liquid Glass on iOS 26+, with our own fallback elsewhere.

## Consequences
- Some native modules need config plugins.
- Heavy real-time 3D is limited on phones: use pre-rendered sequences or Skia 2.5D effects.
- App size and start time need watching.

## Alternatives considered
- **Native Kotlin and Swift:** two codebases.
- **Flutter:** a new language and less reuse with the web app.

## Revisit when
A required native capability is impractical in Expo.
