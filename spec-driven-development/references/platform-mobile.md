# Platform: Mobile app

Load this when C1 = mobile, or for the mobile surface of a hybrid. These are additions to the phase
references. **Verify current tool versions and store policies at Gate 1.5 / Gate 7**: store rules and
SDK minimums change yearly.

The big differences: **old versions live forever** (users don't update), **a third party reviews every
release** (the stores), and **the OS kills, suspends and restricts your app**. Design for all three in
the SPEC, not at release.

## Intake questions (platform round)

| # | Question | Choices (recommended first, from facts) |
|---|---|---|
| M1 | Which platforms? | iOS + Android · iOS only · Android only · Phone-friendly web app instead (PWA) |
| M2 | How do users get it? | Public App Store / Play Store · Internal/enterprise (TestFlight, MDM, private Play track) · Sideload/APK for a few known people · Decide at DEPLOY |
| M3 | Does it need a backend? | Yes, our own API (new) · Yes, an existing API · A BaaS (Supabase/Firebase/PocketBase) · No, on-device only |
| M4 | Must it work offline? | Online required · Read offline, write online · Full offline with sync · On-device only (no network) |
| M5 | Which device features does it need? (multi-select) | Push notifications · Camera/photos · Location (foreground / background) · None of these |
| M5b | Any others? (multi-select) | Biometrics (Face ID/fingerprint) · Contacts/calendar · Bluetooth/NFC · Background tasks/sync |
| M6 | Does money move in the app? | No · Yes, digital goods/subscriptions (store billing rules apply) · Yes, physical goods/services (external payments allowed) |
| M7 | Phones only, or tablets too? | Phones, portrait only · Phones, both orientations · Phones + tablets · Tablet-first |

Follow-ups: M1 includes iOS → is there an Apple Developer Program account (needed for TestFlight and the
App Store)? M2 = public → is there a Google Play developer account? (New personal accounts may need a
closed-testing period with real testers before production access; verify current Play policy.)
Is there a privacy policy URL? Minimum OS versions (default: the versions covering ~90% of the target
audience; check current distribution data).

## SPEC additions
- **App lifecycle:** what happens on background, kill and cold start mid-flow (draft restored? form
  lost?), deep-link entry to every screen that has one, state restoration.
- **Versioned API + minimum supported app version.** The server must serve N-2 app versions (or a
  stated policy) and can force-upgrade below a floor. Without this you can never make a breaking API
  change.
- **Offline (if M4 ≠ online):** the local store schema (a contract like a server schema, with
  migrations), the sync conflict policy, the outbound queue (limits, retries, idempotency keys), what
  the UI shows while pending.
- **Permissions:** for each, *when* it is requested (in context, never at launch), the rationale copy,
  and **what the app does when it's denied**. Denial is a normal path with its own ACs.
- **Push (if M5):** each notification type, trigger, recipient, payload content (no sensitive data in
  the payload), tap destination, and the user's opt-out.
- **§11:** cold-start target, app size budget, battery/data usage stance, minimum OS, supported devices,
  a11y (Dynamic Type / font scaling, screen readers), localisation and RTL.
- **§12 mobile edge cases:** connectivity flapping, app killed during upload, permission revoked in
  Settings while the app is running, low storage, clock tampering, the same account on two devices, an
  old app version hitting a new API, push arriving for a deleted item, OS dark mode switching mid-session.
- **Store compliance as SPEC items:** account deletion in-app if accounts can be created (Apple
  requires it), privacy nutrition label / Play data-safety answers derived from §7, sign in with Apple
  if third-party social login is offered on iOS (check current guideline wording), billing rules for
  M6.

## Stack options

| Option | Fits when | Trade-off |
|---|---|---|
| **React Native + Expo** | Both platforms, TS team, fast iteration, OTA JS updates (EAS Update) | Native modules for edge features; OTA must respect store rules |
| **Flutter** | Both platforms, custom UI, consistent rendering | Dart; platform channels for native features |
| **Native: Swift/SwiftUI + Kotlin/Jetpack Compose** | Deep platform integration, best performance/feel, single platform | Two codebases for both platforms |
| **Kotlin Multiplatform** (shared logic, native UI) | Shared core, native UI each side | More setup; team needs both UIs |
| **PWA** | M1 = web instead; no store, limited device APIs (iOS limits push/background) | Not a mobile app; re-route to `platform-web.md` |

Backend: our own API (see `platform-web.md` for the server side), or a BaaS where §7/§10 fit its model.
Local store: SQLite (expo-sqlite, sqflite, Room, SwiftData/GRDB) or a sync-engine store if M4 = full
offline. Push: FCM (Android, and iOS via APNs) or APNs direct. Expo notifications wraps both.

iOS builds need macOS + Xcode: a local or remote Mac, a macOS CI runner, or a cloud build service
(e.g. Expo EAS). Record which in AGENTS.md (c).

## DESIGN additions
- Navigation model: tabs / stack / drawer, the back behaviour on Android (system back) and iOS
  (swipe-back), deep-link targets.
- Platform conventions: follow iOS HIG and Material where they differ (or a stated custom system
  applied consistently, decided explicitly).
- Touch targets ≥44pt (iOS) / 48dp (Android); thumb reach for primary actions.
- Safe areas, notch/dynamic island, keyboard avoidance on every form, landscape (per M7).
- Font scaling: layouts survive the largest accessibility text size; no fixed-height text containers.
- Offline, pending, sync-failed and permission-denied states drawn for every screen they touch.
- Splash/launch screen, app icon set, notification icon (Android monochrome).
- Haptics and motion: purposeful, respects reduce-motion.

## TESTING tooling
| Level | Default tools |
|---|---|
| Unit | Jest/Vitest (RN) · flutter test · XCTest · JUnit |
| Component | React Native Testing Library · Flutter widget tests · Compose UI tests |
| Integration | App logic against a **real local SQLite** and a **real test API** (docker compose backend) |
| E2E | **Maestro** (cross-platform, YAML flows) · Detox (RN) · XCUITest / Espresso (native) |
| Devices | Emulator + simulator in CI; **at least one physical device per platform** before each release (push, camera and biometrics don't behave the same on simulators) |
| API compatibility | A contract test: the previous app release's API calls replayed against the new server |

Mobile must-tests: kill-and-restore mid-flow; offline → online sync, including conflicts; permission
denied for every permission; a deep link to every linkable screen; the minimum-version force-upgrade
path; local DB migration from the previous release's schema; the largest font size on the key screens.

## SECURITY surface (mobile additions)
- **Never trust the client.** Every rule is enforced server-side; the app binary can be decompiled and
  modified. No secrets in the app bundle (API keys in a bundle are public keys).
- Token storage: Keychain (iOS) / Keystore-backed EncryptedSharedPreferences or equivalent (Android).
  Never AsyncStorage/plain prefs for tokens.
- Transport: TLS only (ATS on iOS, no cleartext on Android); consider cert pinning only with a rotation
  plan (bad pinning bricks the app).
- Deep links: universal links/app links verified by domain; treat every parameter as untrusted.
- Auth: OAuth with PKCE for third-party providers; biometrics gate a local key, not the server auth.
- Push payloads carry no sensitive data (lock-screen visible).
- Screenshot/app-switcher exposure for sensitive screens (FLAG_SECURE / blur on background) if §11
  calls for it.
- Logs: no PII or tokens in device logs; crash reporter scrubbing.
- Store privacy disclosures must match actual data collection, including SDKs (analytics, crash
  reporting). A mismatch gets the app rejected or removed.
- Jailbreak/root detection only if the threat model needs it. Usually it doesn't; don't add theatre.

## PLAN Phase 0 (mobile)
1. Toolchain; app runs on simulator **and** emulator; every AGENTS (d) command is run once.
2. **A signed build delivered through the real channel:** TestFlight internal build + Play
   internal-testing track (or the M2 channel). Provisioning, bundle IDs, signing keys and store
   listings are the long pole and go first.
3. Backend skeleton + versioned API + the minimum-version check endpoint, used by the app on launch.
4. Local store + schema v1 + migration framework (if offline).
5. Push to a physical device end to end (if M5 includes push). APNs keys and FCM config take time.
6. Maestro (or chosen E2E) running one smoke flow in CI.

## DEPLOY specifics (→ "release" in DEPLOY.md)
- Versioning (marketing version + build number), changelog, release notes per store.
- Build: EAS / Xcode Cloud / fastlane / CI on a Mac runner. Signing keys and keystores live in CI
  secrets; **the Android upload key and the keystore backup are irreplaceable**, so DEPLOY says where
  they are kept.
- Tracks: internal → closed/TestFlight external → production with **staged rollout** (Play %
  rollout, App Store phased release).
- Store review time is part of the schedule; build in buffer and have the review notes and test
  account ready.
- OTA updates (Expo): only JS/asset changes, within store rules; native changes need a store release.
  Channel per environment.
- **Rollback reality:** you can halt a staged rollout and ship a fix forward. You can't pull a version
  off devices. The server's minimum-version floor is the emergency brake.
- Backend deploy follows `platform-web.md`. **The backend deploys before the app release that needs it,
  and it stays backward compatible.**
- Crash reporting + analytics with consent as the SPEC decided.
