"""Sending your answers to the chat that asked. Always your own action (a button), never automatic.

Route: DHI Orbit actions.reply (claude attach through a pty for background chats, confirmed by reading
the prompt back from the transcript; refused for a chat open in a terminal tab). A chat that is
working gets the reply queued and sent when it goes idle (contract: "queued if working").
A read-only account (config read_only_accounts) is refused.
"""
from __future__ import annotations

import threading
import time

from . import db, sources

from .. import actions as _actions       # dhi_orbit/actions.py


MAX_QUEUED = 10                        # waiting messages per chat


class Sender:
    def __init__(self, src, reply_fn=None):
        self.src = src
        self.reply_fn = reply_fn or (lambda chat, text: _actions.reply(chat, text, manual=True))   # the user's own message
        self.queue: dict[str, list[dict]] = {}      # session_id -> [{id, text, at, key}], oldest first
        self.lock = threading.Lock()
        self._seq = 0

    def queued(self, session_id: str) -> list[dict]:
        """What is waiting to be typed into this chat, oldest first."""
        with self.lock:
            return [{"id": q["id"], "text": q["text"], "at": q["at"]} for q in self.queue.get(session_id, [])]

    def edit_queued(self, session_id: str, qid: int, text: str | None) -> tuple[int, dict]:
        """Change a waiting message's text, or drop it when text is None. Only what has not been typed in yet."""
        text = None if text is None else text.strip()
        if text is not None and (not text or len(text) > 20000):
            return 400, {"error": "empty reply" if not text else "reply too long"}
        with self.lock:
            items = self.queue.get(session_id, [])
            q = next((x for x in items if x["id"] == qid), None)
            if not q:
                return 409, {"error": "already typed in or removed"}
            if text is None:
                items.remove(q)
                if not items:
                    self.queue.pop(session_id, None)
            else:
                q["text"] = text
        return 200, {"ok": True, "queued": self.queued(session_id)}

    def _chat(self, session_id: str, key: str | None = None) -> dict | None:
        chats = self.src.get()["chats"]
        return next((c for c in chats if (key and c["key"] == key) or c["session_id"] == session_id), None)

    def reply(self, session_id: str, text: str, key: str | None = None) -> tuple[int, dict]:
        text = (text or "").strip()
        if not text:
            return 400, {"error": "empty reply"}
        if len(text) > 20000:
            return 400, {"error": "reply too long"}
        c = self._chat(session_id, key)
        if not c:
            return 404, {"error": "no such session in the last 24 h"}
        if c["excluded"] or sources.excluded(c["config"]):
            return 403, {"error": "this account is read-only here"}
        if c["state"] == "working":
            with self.lock:
                items = self.queue.setdefault(c["session_id"], [])
                if len(items) >= MAX_QUEUED:
                    return 429, {"error": f"{MAX_QUEUED} messages are already waiting for this chat"}
                self._seq += 1
                items.append({"id": self._seq, "text": text, "at": time.time(), "key": c["key"]})
            db.log_auto("reply", "manual", c["session_id"], c["account"], "queued", "chat is working", {"text": text[:400]})
            return 200, {"ok": True, "queued": True, "confirmed": False, "waiting": self.queued(c["session_id"])}
        res = self.reply_fn(c, text)
        db.log_auto("reply", "manual", c["session_id"], c["account"], ("queued" if res.get("queued") else "sent") if res.get("ok") else "failed",
                    res.get("error") or res.get("route") or "", {"text": text[:400], "result": res})
        if not res.get("ok"):
            return 409, {"error": res.get("error") or "not delivered", "route": res.get("route")}
        return 200, {"ok": True, "queued": bool(res.get("queued")), "confirmed": bool(res.get("confirmed")), "route": res.get("route")}

    def drain(self) -> list[dict]:
        """Send queued replies whose chat is no longer working. Called from the refresh loop."""
        done = []
        with self.lock:
            items = [(sid, qs[0]) for sid, qs in self.queue.items() if qs]
        for sid, q in items:        # one per chat per pass: once it is typed in the chat is working again, the next waits
            c = self._chat(sid, q["key"])
            if not c or c["state"] in ("working", "needs_you"):
                continue
            with self.lock:
                cur = self.queue.get(sid) or []
                if not cur or cur[0]["id"] != q["id"]:      # edited or removed since the snapshot: take what is there now
                    continue
                cur.pop(0)
                if not cur:
                    self.queue.pop(sid, None)
            code, res = self.reply(sid, q["text"], q["key"])
            done.append({"session_id": sid, "code": code, **res})
        return done
