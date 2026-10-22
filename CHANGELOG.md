# Changelog

User-visible changes per release, newest first. Full notes with links: [Releases](https://github.com/Dv04/dhi-orbit/releases).

## 0.3.17 (2026-10-14)
- Dictation no longer brings back a sent prompt or leaks into another chat.
- The permission dialog card never offers a free-text box; "Open in Terminal" is offered while its options are not read yet.
- The login page names the real access key.

## 0.3.16 (2026-10-10)
- Documents reader beside every chat: the Markdown files a chat made or pointed to, with tables, highlighted code, an outline and links between documents.

## 0.3.15 (2026-10-09)
- A background shell no longer blocks replies; a shell ring shows on chat dots.
- New chat takes attachments and a sticky interview tick; open proposals stay open.

## 0.3.14 (2026-10-08)
- PyPI summary names Gemini CLI and Antigravity; the README, screenshots and sponsor links reach the PyPI page.

## 0.3.13 (2026-10-07)
- Orbit logo in the dashboard and as the tab icon.

## 0.3.12 (2026-10-07)
- Capacity view: 4.8% of the 7-day limit unlocks every 8 hours; "Use first" needs 10 points; "Ahead of pace" at 5 or more points over.
- Logo in the README, dashboard icon and PWA manifest.

## 0.3.11 (2026-10-07)
- Codex and Cursor seats no longer appear with Claude chats; Codex usage limits added; tested Windows package.
- `tools/release.sh`: checked, repeatable release.

## 0.3.10 (2026-10-07)
- Settings > Quality: frame-rate limit, render resolution, nebula detail, particles, glow, glass blur, animation switches, and Low / Balanced / High / Ultra presets.

## 0.3.8 (2026-10-07)
- Codex and Cursor chats on the same board, labelled by tool.
- Windows support (beta): ConPTY terminal layer through `pywinpty`.
- `--open` opens the dashboard in your browser; Ctrl+C stops it cleanly.

## 0.3.7 (2026-10-06)
- Dashboard at `http://127.0.0.1:8787/` (no `/v2/`); `/v2/` still works.
- Settings > Report a bug or send feedback (opens a prefilled GitHub issue; nothing is sent from the dashboard).
- New chat dialog with work-item picker; file attachments on replies (25 MB cap, deleted after 30 days); resizable chat split; `?` shortcut sheet; phone layout fixes.

## 0.3.3 to 0.3.6 (2026-10-06)
- Graph views refresh while open; the waiting chain marks chats parked behind a seat at a limit.
- Audit fixes: the Stop-hook evidence check no longer crashes on long commands, malformed query parameters answer 400, closed tabs no longer log tracebacks.
