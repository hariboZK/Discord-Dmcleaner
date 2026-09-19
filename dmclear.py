#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════
#   DMCLEAR  —  Discord Mesaj Silici
#   Seçilen kanalda kendi mesajlarını siler
#   Made By Haribo
# ══════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import time
import random
from datetime import datetime

# ─── Renkler ─────────────────────────────────
BG     = "#0a0a0a"
BG2    = "#111111"
BG3    = "#1a1a2e"
ACCENT = "#5865f2"
TEXT   = "#dcddde"
SUB    = "#72767d"
GREEN  = "#57f287"
YELLOW = "#fee75c"
RED    = "#ed4245"
BLUE   = "#00b0f4"

API = "https://discord.com/api/v9"

def snowflake_to_time(sf_id):
    try:
        return datetime.utcfromtimestamp(((int(sf_id) >> 22) + 1420070400000) / 1000)
    except Exception:
        return datetime.utcnow()


class DMClear(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DMCLEAR  --  Discord Mesaj Silici  |  Made By Haribo")
        self.geometry("900x720")
        self.minsize(750, 600)
        self.configure(bg=BG)
        self._running = False
        self._paused  = False
        self._my_id   = None
        self._token   = ""
        self._headers = {}
        self._deleted = 0
        self._scanned = 0
        self._skipped = 0
        self._limit   = 0
        self._delay_ms = 800
        self._kw      = ""
        self._dm_map  = {}
        self._style()
        self._build()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TProgressbar", troughcolor=BG3, background=ACCENT, thickness=14)

    def _btn(self, parent, text, cmd, color=ACCENT, w=14):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="#fff", activebackground=color,
                         activeforeground="#fff", relief="flat", bd=0,
                         font=("Consolas", 9, "bold"),
                         cursor="hand2", width=w, pady=5)

    def _entry(self, parent, width=28, default="", show=""):
        e = tk.Entry(parent, width=width, bg=BG3, fg=TEXT,
                     insertbackground=TEXT, relief="flat", bd=4,
                     font=("Consolas", 10), show=show)
        if default:
            e.insert(0, default)
        return e

    def _lf(self, parent, text, color=ACCENT):
        return tk.LabelFrame(parent, text=f"  {text}  ", bg=BG, fg=color,
                             font=("Consolas", 9, "bold"), bd=1, relief="groove")

    def _log(self, msg, tag=""):
        self.log_w.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_w.insert("end", f"[{ts}] {msg}\n", tag if tag else ())
        self.log_w.see("end")
        self.log_w.configure(state="disabled")

    def _clear_log(self):
        self.log_w.configure(state="normal")
        self.log_w.delete("1.0", "end")
        self.log_w.configure(state="disabled")

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG2, height=52)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="DMCLEAR", bg=BG2, fg=ACCENT,
                 font=("Consolas", 18, "bold")).pack(side="left", padx=16, pady=10)
        tk.Label(hdr, text="Discord Mesaj Silici", bg=BG2, fg=SUB,
                 font=("Consolas", 11)).pack(side="left", pady=14)
        tk.Label(hdr, text="Made By Haribo", bg=BG2, fg=SUB,
                 font=("Consolas", 9)).pack(side="right", padx=16)
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x")

        # ─── BÜYÜK BAŞLATMA VE KONTROL PANELİ (EN ÜSTTE - HER ZAMAN GÖRÜNÜR) ───
        top_ctrl = tk.Frame(self, bg=BG2)
        top_ctrl.pack(fill="x", padx=14, pady=(6, 2))

        self.btn_main_start = tk.Button(
            top_ctrl, text="▶  SİLMEYİ BAŞLAT", command=self._start,
            bg="#23a55a", fg="#ffffff", activebackground="#1b8246",
            activeforeground="#ffffff", relief="flat", bd=0,
            font=("Consolas", 12, "bold"), cursor="hand2", padx=22, pady=7
        )
        self.btn_main_start.pack(side="left", padx=(4, 8), pady=3)

        self.btn_main_pause = tk.Button(
            top_ctrl, text="⏸ DURAKLAT", command=self._toggle_pause,
            bg=YELLOW, fg="#000000", activebackground="#d4be48",
            activeforeground="#000000", relief="flat", bd=0,
            font=("Consolas", 10, "bold"), cursor="hand2", padx=14, pady=7
        )
        self.btn_main_pause.pack(side="left", padx=4, pady=3)

        self.btn_main_stop = tk.Button(
            top_ctrl, text="⏹ DURDUR", command=self._stop,
            bg=RED, fg="#ffffff", activebackground="#b82e31",
            activeforeground="#ffffff", relief="flat", bd=0,
            font=("Consolas", 10, "bold"), cursor="hand2", padx=14, pady=7
        )
        self.btn_main_stop.pack(side="left", padx=4, pady=3)

        self.status_v = tk.StringVar(value="Hazır - Token & Kanal seçip 'SİLMEYİ BAŞLAT'a bas")
        tk.Label(top_ctrl, textvariable=self.status_v, bg=BG2, fg=GREEN,
                 font=("Consolas", 10, "bold")).pack(side="left", padx=12)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=8)

        # Sol panel
        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="y", padx=(0, 10))

        # Token
        tok_lf = self._lf(left, "Discord User Token", RED)
        tok_lf.pack(fill="x", pady=4)
        self.tok_e = self._entry(tok_lf, width=34, show=".")
        self.tok_e.pack(fill="x", padx=6, pady=4)
        tok_row = tk.Frame(tok_lf, bg=BG)
        tok_row.pack(fill="x", padx=6, pady=(0,5))
        self.show_v = tk.BooleanVar()
        tk.Checkbutton(tok_row, text="Goster", variable=self.show_v,
                       command=lambda: self.tok_e.config(show="" if self.show_v.get() else "."),
                       bg=BG, fg=SUB, selectcolor=BG3,
                       activebackground=BG, font=("Consolas", 9)).pack(side="left")
        self._btn(tok_row, "Baglan", self._connect, color=GREEN, w=10).pack(side="right")
        self.user_lbl = tk.StringVar(value="Bagli degil")
        tk.Label(left, textvariable=self.user_lbl, bg=BG, fg=SUB,
                 font=("Consolas", 9), anchor="w").pack(fill="x", pady=(0,6))

        # Channel ID
        ch_lf = self._lf(left, "Hedef Kanal ID", YELLOW)
        ch_lf.pack(fill="x", pady=4)
        ch_row = tk.Frame(ch_lf, bg=BG)
        ch_row.pack(fill="x", padx=6, pady=6)
        self.ch_e = self._entry(ch_row, width=22)
        self.ch_e.pack(side="left", padx=(0,6))
        self._btn(ch_row, "Bilgi", self._ch_info, color="#334", w=8).pack(side="left")
        self.ch_lbl = tk.StringVar(value="")
        tk.Label(ch_lf, textvariable=self.ch_lbl, bg=BG, fg=BLUE,
                 font=("Consolas", 8), anchor="w", wraplength=280).pack(fill="x", padx=6, pady=(0,4))

        # DM listesi
        dm_lf = self._lf(left, "DM Kanallari (Otomatik)", SUB)
        dm_lf.pack(fill="x", pady=4)
        self._btn(dm_lf, "DM Listesini Cek", self._fetch_dms,
                  color=ACCENT, w=22).pack(padx=6, pady=(6,3))
        lb_fr = tk.Frame(dm_lf, bg=BG3)
        lb_fr.pack(fill="x", padx=6, pady=(0,6))
        self.dm_lb = tk.Listbox(lb_fr, bg=BG3, fg=TEXT,
                                font=("Consolas", 9), height=5,
                                selectmode="single",
                                selectbackground=ACCENT)
        self.dm_lb.pack(side="left", fill="x", expand=True)
        dm_sb = ttk.Scrollbar(lb_fr, command=self.dm_lb.yview)
        dm_sb.pack(side="right", fill="y")
        self.dm_lb.configure(yscrollcommand=dm_sb.set)
        self.dm_lb.bind("<<ListboxSelect>>", self._dm_selected)

        # Filtreler
        flt_lf = self._lf(left, "Filtreler", BLUE)
        flt_lf.pack(fill="x", pady=6)
        f1 = tk.Frame(flt_lf, bg=BG); f1.pack(fill="x", padx=6, pady=3)
        tk.Label(f1, text="Limit (0=hepsi):", bg=BG, fg=SUB,
                 font=("Consolas", 9)).pack(side="left")
        self.limit_e = self._entry(f1, width=8, default="0")
        self.limit_e.pack(side="left", padx=4)

        f2 = tk.Frame(flt_lf, bg=BG); f2.pack(fill="x", padx=6, pady=3)
        tk.Label(f2, text="Icerik filtresi:", bg=BG, fg=SUB,
                 font=("Consolas", 9)).pack(side="left")
        self.kw_e = self._entry(f2, width=16, default="")
        self.kw_e.pack(side="left", padx=4)

        f3 = tk.Frame(flt_lf, bg=BG); f3.pack(fill="x", padx=6, pady=3)
        tk.Label(f3, text="Gecikme (ms):", bg=BG, fg=SUB,
                 font=("Consolas", 9)).pack(side="left")
        self.delay_e = self._entry(f3, width=6, default="800")
        self.delay_e.pack(side="left", padx=4)
        self.delay_lbl = tk.StringVar(value="800ms")
        tk.Label(f3, textvariable=self.delay_lbl, bg=BG, fg=YELLOW,
                 font=("Consolas", 9, "bold")).pack(side="left", padx=4)

        # Slider
        f3b = tk.Frame(flt_lf, bg=BG); f3b.pack(fill="x", padx=6, pady=2)
        self.delay_slider = tk.Scale(
            f3b, from_=0, to=3000, orient="horizontal",
            bg=BG, fg=TEXT, troughcolor=BG3, activebackground=ACCENT,
            highlightthickness=0, font=("Consolas", 7),
            length=240, showvalue=False,
            command=self._on_slider
        )
        self.delay_slider.set(800)
        self.delay_slider.pack(side="left")

        # Hiz preset butonlari
        f4 = tk.Frame(flt_lf, bg=BG); f4.pack(fill="x", padx=6, pady=(4,6))
        tk.Label(f4, text="Hiz:", bg=BG, fg=SUB,
                 font=("Consolas", 9)).pack(side="left", padx=(0,4))
        presets = [
            ("YAVASS",  1500, "#553300"),
            ("NORMAL",   800, "#334"),
            ("HIZLI",    400, "#005533"),
            ("TURBO",    150, "#aa4400"),
            ("MAX",        0, RED),
        ]
        for label, ms, col in presets:
            self._btn(f4, label,
                      lambda m=ms: self._set_speed(m),
                      color=col, w=7).pack(side="left", padx=2)
        tk.Label(f4, text="  MAX=ban riski!", bg=BG, fg=RED,
                 font=("Consolas", 8)).pack(side="left", padx=4)

        # Stats
        stat = tk.Frame(left, bg=BG3)
        stat.pack(fill="x", pady=8)
        self.del_v  = tk.StringVar(value="0")
        self.scan_v = tk.StringVar(value="0")
        self.skip_v = tk.StringVar(value="0")
        for col, (lbl, var, clr) in enumerate([
            ("Silindi",  self.del_v,  GREEN),
            ("Tarandi",  self.scan_v, BLUE),
            ("Atlandi",  self.skip_v, YELLOW),
        ]):
            c = tk.Frame(stat, bg=BG3)
            c.grid(row=0, column=col, padx=10, pady=8, sticky="nsew")
            stat.columnconfigure(col, weight=1)
            tk.Label(c, text=lbl, bg=BG3, fg=SUB,
                     font=("Consolas", 8)).pack()
            tk.Label(c, textvariable=var, bg=BG3, fg=clr,
                     font=("Consolas", 18, "bold")).pack()

        # Kontrol
        ctrl = tk.Frame(left, bg=BG)
        ctrl.pack(fill="x", pady=4)
        self._btn(ctrl, "▶ BAŞLAT", self._start, color=GREEN, w=11).pack(side="left", padx=2)
        self._btn(ctrl, "⏸ DURAKLAT", self._toggle_pause, color=YELLOW, w=11).pack(side="left", padx=2)
        self._btn(ctrl, "⏹ DURDUR",   self._stop, color=RED, w=10).pack(side="left", padx=2)

        self.prog_var = tk.DoubleVar(value=0)
        self.prog = ttk.Progressbar(left, variable=self.prog_var,
                                    maximum=100, mode="indeterminate")
        self.prog.pack(fill="x", pady=(4,0))
        tk.Label(left, textvariable=self.status_v, bg=BG, fg=SUB,
                 font=("Consolas", 9), anchor="w").pack(fill="x")

        # Sag panel: Log
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)
        log_hdr = tk.Frame(right, bg=BG); log_hdr.pack(fill="x", pady=(0,4))
        tk.Label(log_hdr, text="LOG", bg=BG, fg=GREEN,
                 font=("Consolas", 10, "bold")).pack(side="left")
        self._btn(log_hdr, "Temizle", self._clear_log, color="#222", w=9).pack(side="right")
        self.log_w = scrolledtext.ScrolledText(
            right, bg=BG3, fg=GREEN, font=("Consolas", 9),
            state="disabled", relief="flat", bd=0, wrap="word"
        )
        self.log_w.pack(fill="both", expand=True)
        self.log_w.tag_config("del",  foreground=GREEN)
        self.log_w.tag_config("skip", foreground=SUB)
        self.log_w.tag_config("err",  foreground=RED)
        self.log_w.tag_config("info", foreground=BLUE)
        self.log_w.tag_config("warn", foreground=YELLOW)

    # ── Hiz Presetleri ────────────────────────
    def _set_speed(self, ms: int):
        self.delay_e.delete(0, "end")
        self.delay_e.insert(0, str(ms))
        self.delay_slider.set(ms)
        labels = {0: "MAX (tehlikeli!)", 150: "TURBO",
                  400: "HIZLI", 800: "NORMAL", 1500: "YAVASS"}
        self.delay_lbl.set(labels.get(ms, f"{ms}ms"))
        if self._running:
            self._delay_ms = max(0, ms)

    def _on_slider(self, val):
        ms = int(float(val))
        self.delay_e.delete(0, "end")
        self.delay_e.insert(0, str(ms))
        self.delay_lbl.set(f"{ms}ms")
        if self._running:
            self._delay_ms = max(0, ms)

    # ── Baglan ────────────────────────────────
    def _connect(self):
        token = self.tok_e.get().strip()
        if not token: return
        self._token   = token
        self._headers = {
            "Authorization": token,
            "Content-Type":  "application/json",
            "User-Agent":    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        def w():
            try:
                r = requests.get(f"{API}/users/@me", headers=self._headers, timeout=6)
                if r.status_code == 200:
                    me = r.json()
                    self._my_id = me["id"]
                    name = me["username"] + "#" + me.get("discriminator", "0")
                    self.user_lbl.set(f"Baglandi: {name}  (ID:{self._my_id})")
                    self._log(f"Token OK: {name}", "info")
                    self.status_v.set(f"Baglandi: {name}")
                else:
                    self.user_lbl.set("HATA: Token gecersiz!")
                    self._log(f"Token hatasi: HTTP {r.status_code}", "err")
            except Exception as e:
                self._log(f"Baglanamadi: {e}", "err")
        threading.Thread(target=w, daemon=True).start()

    # ── Kanal Bilgisi ─────────────────────────
    def _ch_info(self):
        cid = self.ch_e.get().strip()
        if not cid or not self._my_id: return
        def w():
            try:
                r = requests.get(f"{API}/channels/{cid}", headers=self._headers, timeout=6)
                if r.status_code == 200:
                    d = r.json()
                    ch_type = d.get("type", "?")
                    if ch_type == 1:
                        recip = d.get("recipients", [{}])[0]
                        name = f"DM: {recip.get('username','?')}"
                    elif ch_type == 0:
                        name = f"#{d.get('name','?')} (Sunucu kanali)"
                    else:
                        name = f"Kanal tip:{ch_type}"
                    self.ch_lbl.set(f"-> {name}")
                    self._log(f"Kanal: {name}  ID:{cid}", "info")
                else:
                    self.ch_lbl.set(f"Hata: HTTP {r.status_code}")
            except Exception as e:
                self._log(f"Hata: {e}", "err")
        threading.Thread(target=w, daemon=True).start()

    # ── DM Listesi ────────────────────────────
    def _fetch_dms(self):
        if not self._my_id:
            messagebox.showwarning("Uyari", "Once token ile baglan!")
            return
        def w():
            try:
                r = requests.get(f"{API}/users/@me/channels", headers=self._headers, timeout=8)
                if r.status_code != 200:
                    self._log(f"DM listesi alinamadi: {r.status_code}", "err"); return
                channels = r.json()
                self.dm_lb.delete(0, "end")
                self._dm_map.clear()
                count = 0
                for ch in channels:
                    if ch.get("type") != 1: continue
                    recips = ch.get("recipients", [{}])
                    uname  = recips[0].get("username", "?") if recips else "?"
                    display = f"{uname}  [{ch['id']}]"
                    self._dm_map[display] = ch["id"]
                    self.dm_lb.insert("end", display)
                    count += 1
                self._log(f"{count} DM kanali listelendi", "info")
            except Exception as e:
                self._log(f"Hata: {e}", "err")
        threading.Thread(target=w, daemon=True).start()

    def _dm_selected(self, event=None):
        sel = self.dm_lb.curselection()
        if not sel: return
        display = self.dm_lb.get(sel[0])
        cid = self._dm_map.get(display, "")
        if cid:
            self.ch_e.delete(0, "end")
            self.ch_e.insert(0, cid)
            self.ch_lbl.set(f"-> {display}")

    # ── Başlat / Durdur ───────────────────────
    def _start(self):
        token = self.tok_e.get().strip()
        if not token:
            messagebox.showwarning("Uyarı", "Discord User Token girmedin!\nLütfen önce token'ını kutuya yapıştır.")
            return

        cid = self.ch_e.get().strip()
        if not cid:
            # Listede seçili DM var mı kontrol et
            sel = self.dm_lb.curselection()
            if sel:
                display = self.dm_lb.get(sel[0])
                cid = self._dm_map.get(display, "")
                if cid:
                    self.ch_e.delete(0, "end")
                    self.ch_e.insert(0, cid)

        if not cid:
            messagebox.showwarning("Uyarı", "Kanal ID girmedin!\nLütfen bir Kanal ID yaz veya 'DM Listesini Çek' butonuna basıp bir kişi seç.")
            return

        if self._running:
            messagebox.showinfo("Bilgi", "Silme işlemi zaten çalışıyor!")
            return

        # Token otomatik bağlanma kontrolü
        if not self._my_id or self._token != token:
            self._token   = token
            self._headers = {
                "Authorization": token,
                "Content-Type":  "application/json",
                "User-Agent":    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            self.status_v.set("Token doğrulanıyor...")
            self.update_idletasks()
            try:
                r = requests.get(f"{API}/users/@me", headers=self._headers, timeout=6)
                if r.status_code == 200:
                    me = r.json()
                    self._my_id = me["id"]
                    name = me["username"] + "#" + me.get("discriminator", "0")
                    self.user_lbl.set(f"Bağlandı: {name} (ID:{self._my_id})")
                    self._log(f"Token onaylandı: {name}", "info")
                else:
                    messagebox.showerror("Hata", f"Token geçersiz! (HTTP {r.status_code})\nLütfen doğru Discord user token gir.")
                    self.status_v.set("Hata: Token geçersiz")
                    return
            except Exception as e:
                messagebox.showerror("Hata", f"Discord'a bağlanılamadı:\n{e}")
                self.status_v.set("Hata: Bağlantı kurulamadı")
                return

        try:
            self._limit = int(self.limit_e.get().strip() or "0")
        except ValueError:
            self._limit = 0
        try:
            self._delay_ms = max(0, int(self.delay_e.get().strip() or "800"))
        except ValueError:
            self._delay_ms = 800
        self._kw      = self.kw_e.get().strip().lower()
        self._running = True
        self._paused  = False
        self._deleted = 0
        self._scanned = 0
        self._skipped = 0
        self.del_v.set("0"); self.scan_v.set("0"); self.skip_v.set("0")
        self.prog.configure(mode="indeterminate"); self.prog.start(12)
        self.status_v.set("▶ Siliniyor...")
        self._log(f"Başlatıldı | Kanal: {cid} | Limit: {self._limit or 'Sınırsız'} | Gecikme: {self._delay_ms}ms", "info")
        threading.Thread(target=self._worker, args=(cid,), daemon=True).start()

    def _toggle_pause(self):
        if not self._running: return
        self._paused = not self._paused
        if self._paused:
            self.status_v.set("Duraklatildi")
            self._log("Duraklatildi", "warn")
        else:
            self.status_v.set("Devam ediyor...")
            self._log("Devam ediyor", "info")

    def _stop(self):
        self._running = False
        self._paused  = False
        self.prog.stop()
        self.status_v.set(f"Durduruldu | Silindi:{self._deleted}")
        self._log(f"Durduruldu | Tarandi:{self._scanned} Silindi:{self._deleted} Atlandi:{self._skipped}", "warn")

    # ── Worker ────────────────────────────────
    def _worker(self, channel_id):
        before_id = None
        while self._running:
            while self._paused and self._running:
                time.sleep(0.5)
            if not self._running: break

            params = {"limit": 100}
            if before_id:
                params["before"] = before_id
            try:
                r = requests.get(f"{API}/channels/{channel_id}/messages",
                                 headers=self._headers, params=params, timeout=10)
            except Exception as e:
                self._log(f"Fetch hata: {e}", "err"); time.sleep(3); continue

            if r.status_code == 429:
                retry = r.json().get("retry_after", 2)
                self._log(f"Rate limit! {retry:.1f}s bekleniyor...", "warn")
                time.sleep(float(retry) + 0.5); continue

            if r.status_code != 200:
                self._log(f"Mesaj alinamadi: HTTP {r.status_code}", "err"); break

            messages = r.json()
            if not messages:
                self._log("Daha fazla mesaj yok -- tamamlandi.", "info"); break

            before_id   = messages[-1]["id"]
            found_mine  = False

            for msg in messages:
                if not self._running: break
                while self._paused and self._running:
                    time.sleep(0.5)

                self._scanned += 1
                self.scan_v.set(str(self._scanned))

                if msg.get("author", {}).get("id") != self._my_id:
                    self._skipped += 1
                    self.skip_v.set(str(self._skipped))
                    continue

                found_mine = True
                content = msg.get("content", "")

                if self._kw and self._kw not in content.lower():
                    self._skipped += 1
                    self.skip_v.set(str(self._skipped))
                    continue

                if self._limit and self._deleted >= self._limit:
                    self._log(f"Limite ulasildi ({self._limit})", "warn")
                    self._running = False; break

                self._delete_msg(channel_id, msg["id"], content)
                delay = self._delay_ms / 1000.0
                if delay > 0:
                    delay += random.uniform(-0.05, 0.12)
                    time.sleep(max(0, delay))

            if not found_mine and len(messages) < 100:
                self._log("Tum mesajlar tarandi.", "info"); break

        self._running = False
        self.prog.stop()
        self.prog.configure(mode="determinate")
        self.prog_var.set(100)
        self.status_v.set(f"Tamamlandi | Silindi:{self._deleted}")
        self._log(f"Bitti | Tarandi:{self._scanned} Silindi:{self._deleted} Atlandi:{self._skipped}", "info")

    def _delete_msg(self, channel_id, msg_id, content):
        preview = content[:45].replace("\n", " ") if content else "[bos]"
        ts_msg  = snowflake_to_time(msg_id).strftime("%Y-%m-%d %H:%M")
        try:
            r = requests.delete(f"{API}/channels/{channel_id}/messages/{msg_id}",
                                headers=self._headers, timeout=8)
            if r.status_code in [200, 204]:
                self._deleted += 1
                self.del_v.set(str(self._deleted))
                self._log(f"[SILINDI] [{ts_msg}] {preview}", "del")
            elif r.status_code == 429:
                retry = r.json().get("retry_after", 2)
                self._log(f"Rate limit {retry:.1f}s", "warn")
                time.sleep(float(retry) + 0.3)
                self._delete_msg(channel_id, msg_id, content)
            elif r.status_code == 404:
                self._log(f"[404] Zaten yok: {msg_id}", "skip")
            else:
                self._log(f"[HATA] HTTP {r.status_code} | {msg_id}", "err")
        except Exception as e:
            self._log(f"[HATA] {e}", "err")


if __name__ == "__main__":
    app = DMClear()
    app.mainloop()
