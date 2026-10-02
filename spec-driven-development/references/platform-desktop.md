# Platform: Desktop app

Load this when C1 = desktop, or for the desktop surface of a hybrid. These are additions to the phase
references. **Verify current tool versions at Gate 1.5**; never pin from memory.

The big difference from web: **you ship binaries to machines you don't control, and you can't take a
release back.** Packaging, signing, auto-update and on-disk data formats are SPEC-level decisions, not
deploy details.

## Intake questions (platform round)

| # | Question | Choices (recommended first, from facts) |
|---|---|---|
| D1 | Which operating systems? | macOS only · macOS + Windows · macOS + Windows + Linux · Linux only |
| D2 | Where does the data live? | Only on this machine (local-first, no account) · Local + sync to a server/cloud · Server is the source; the app is a client · Files the user opens/saves (document-based) |
| D3 | What must it touch on the machine? | Nothing special · User-chosen files/folders · Background/tray, starts at login · Hardware (USB, serial, camera, GPU), system APIs, or other apps |
| D4 | How do users get it and get updates? | Download from a site + built-in auto-update · Mac App Store / Microsoft Store · Package managers (Homebrew/winget/apt) · Internal distribution only |
| D5 | How should it look and feel? | Native-feeling per OS · One consistent custom look everywhere · Mostly a web-style UI is fine |
| D6 | Must it work fully offline? | Yes, offline is normal · Mostly offline, syncs when online · Online required |

Follow-ups: D1 includes macOS + direct download → there's an Apple Developer account for Developer ID
signing + notarization (yes / no / get one). D1 includes Windows → code-signing certificate (yes / no /
unsigned for internal use; SmartScreen warnings are the cost). D3 = hardware → which devices exactly,
and are they available for testing?

## SPEC additions
- **§7 persisted format is a contract.** File formats and local DB schemas outlive app versions:
  versioned schema, a migration on launch, a forward-compatibility stance (what an old app does with a
  newer file), and corruption recovery.
- **Where data lives on disk** per OS (app data dir, documents, cache), plus what is backed up and what
  is disposable.
- **Process model:** single instance? Tray/background? Starts at login? Multiple windows?
- **§9 becomes IPC:** the commands the UI can invoke in the core/main process, with their arguments
  and the permission each needs. This is the security boundary (see SECURITY).
- **Update policy:** auto-update channel(s) (stable/beta), forced versus optional updates, minimum
  supported version if a server exists, behaviour when an update fails.
- **Sync (if D2 = sync):** conflict resolution policy (last-write-wins / per-field merge / CRDT /
  manual), what is authoritative, offline queue limits, an identity/account model.
- **§11:** cold-start time, memory footprint, installer size budget, OS minimum versions, HiDPI,
  multi-monitor.
- **§12 desktop edge cases:** app killed mid-write (atomic writes), disk full, file deleted or moved
  under the app, two instances, sleep/wake, clock change, permission denied, network flapping, the
  user downgrades the app.

## Stack options

| Option | Fits when | Trade-off |
|---|---|---|
| **Tauri** (Rust core + web UI) | Cross-platform, small binaries, strong IPC permission model | Rust in the core; per-OS webview differences |
| **Electron** (Node + Chromium) | Heavy web-ecosystem reuse, identical rendering everywhere | Size/memory; IPC/`nodeIntegration` hardening is on you |
| **Native: SwiftUI** (macOS) / **WinUI/.NET** (Windows) | Single OS, deepest OS integration, best feel | One codebase per OS |
| **Flutter desktop / Compose Multiplatform / .NET MAUI / Avalonia** | Shared code with mobile, custom UI | Less native feel; desktop maturity varies |
| **Qt** (C++/Python) | Hardware-heavy, long-lived industrial apps | Licensing (LGPL/commercial), C++ |

Local storage: SQLite (default for structured data) · plain files with atomic write-and-rename ·
embedded KV. Sync: your own API, or a sync engine (e.g. CRDT libs, ElectricSQL/PowerSync-style) if D2
demands it. **Choose from §7/§8, not taste.**

macOS builds, signing and notarization need a Mac with Xcode (local, remote, or a macOS CI runner).
Record which one in AGENTS.md (c).

## DESIGN additions
- Window model: default/min size, resizable, restore position, multi-window behaviour.
- Native menus (macOS app menu, Windows menu bar or none), the shortcut map per OS (Cmd vs Ctrl),
  context menus.
- System integration surfaces: tray/menu-bar icon and menu, notifications, dock badge, file
  associations, drag-and-drop in/out.
- Light/dark follows the OS by default (ask); high-contrast mode on Windows.
- Per-OS conventions where D5 = native-feeling: button order in dialogs, window controls, settings
  placement (Preferences vs Settings).
- Every long operation: progress, cancellable, what happens on quit mid-operation.

## TESTING tooling
| Level | Default tools |
|---|---|
| Unit | Language-native (cargo test, Vitest, XCTest, xUnit) |
| Integration | Core logic against a **real SQLite/files in a temp dir**; IPC commands invoked directly |
| E2E | Tauri: WebDriver (tauri-driver) · Electron: Playwright's Electron support · Native macOS: XCUITest · Windows: WinAppDriver/Appium |
| Packaging | Build installers for every OS in CI; install → launch → smoke → uninstall on a clean VM/runner |
| Update | Install version N, publish N+1 to a test channel, verify auto-update and the data migration |

Desktop must-tests: **data migration from every previously released schema version** (keep fixture
files from each release); atomic write survives a kill mid-save; the app starts with a corrupted or
missing data file and recovers as SPEC says; a single-instance lock.

**A real OS matrix is part of done.** "Works on my Mac" proves macOS on one version. CI runners per OS
are the minimum; at least one manual smoke on a clean machine per OS before release.

## SECURITY surface (desktop additions)
- **IPC is the attack surface.** Allow-list commands; validate every argument in the core; no generic
  "run this" or "read any path" command. Tauri capabilities/permissions scoped per window; Electron:
  `contextIsolation: true`, `nodeIntegration: false`, sandbox, a narrow `contextBridge`.
- Webview content: never load remote content into a privileged window; CSP; `shell.openExternal` only
  for allow-listed URL schemes.
- **Code signing and notarization** (macOS Developer ID + notarization; Windows Authenticode). Signing
  keys never in the repo; they live in CI secrets or a hardware token.
- **Update integrity:** signed update manifests, verified before install, HTTPS only. A compromised
  update channel is a remote code execution channel for every install.
- Secrets on disk: OS keychain (Keychain, Credential Manager, libsecret), never plaintext config.
- Local data at rest: is encryption needed? (Laptops get stolen.) File permissions on the app data dir.
- Deep links / URL scheme handlers: treat them as untrusted input.
- Dependency supply chain: the native module ecosystem (npm postinstall, crates build.rs).

## PLAN Phase 0 (desktop)
1. Toolchain + an empty window launching on **every target OS** (CI matrix).
2. **The signed + packaged "hello world" through the real pipeline:** sign, notarize (macOS), install
   on a clean machine, launch. This is the long pole; it goes first.
3. Auto-update: ship v0.0.1 → v0.0.2 through the real update channel before features exist.
4. Local storage + schema v1 + migration framework + the "open a v1 file" fixture test.
5. The IPC boundary skeleton with one allow-listed command and its permission test.

## DEPLOY specifics (→ "release" in DEPLOY.md)
- Versioning scheme, changelog, release channels (beta/stable).
- The build matrix and where each artefact is built (macOS builds need macOS).
- Signing steps per OS, notarization + stapling, checksum publication.
- Distribution: download host, update feed, store submissions (separate review timelines).
- **Rollback reality:** you can't un-ship a binary. You can pull the update feed, ship a fix forward,
  and (if a server exists) enforce a minimum version. DEPLOY.md states this honestly.
- Crash reporting (Sentry or similar) with PII scrubbing. Decide whether it's opt-in.
