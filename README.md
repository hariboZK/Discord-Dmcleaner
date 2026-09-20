<div align="center">

# 🧹 DMCLEAR — Discord Message Purger

**A sleek, Discord-themed GUI tool to bulk delete your own messages from DMs, Group Chats, and Server Channels.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-5865F2?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![Author](https://img.shields.io/badge/author-Haribo-5865f2.svg?style=for-the-badge)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

[Features](#-features) • [Speed Presets](#-speed-presets) • [Installation](#-installation) • [Usage](#-usage) • [Rate Limits & Safety](#-rate-limits--safety) • [Disclaimer](#-disclaimer)

</div>

---

## ✨ Features

- 👤 **Self-Message Purging:** Only deletes messages sent by your account — never touches other users' messages.
- 📩 **Automatic DM Channel Fetcher:** Pulls your recent Direct Messages list automatically with recipient usernames.
- 🎯 **Target Server or Group Channels:** Works on DMs, Group DMs, and any Server Channel where you have message history.
- 🔍 **Keyword & Content Filter:** Delete only messages containing specific keywords or phrases (or leave blank to delete all).
- 🔢 **Custom Message Limit:** Set a maximum message deletion quota or set to `0` to wipe everything.
- ⚡ **Dynamic Speed Controls:** Slider and preset buttons ranging from safe (1500ms) to instant turbo modes.
- 🛡️ **Smart Rate-Limit (429) Handling:** Automatically pauses and waits when Discord API rate limits trigger.
- 📊 **Real-Time Live Dashboard:** Displays live counters for Scanned, Deleted, and Skipped messages, alongside a timestamped console log.
- ⏸️ **Interactive Controls:** Pause, Resume, or Abort the deletion process at any time with zero data corruption.

---

## 🏎️ Speed Presets

| Preset | Delay (ms) | Speed | Safety Level | Description |
| :--- | :--- | :--- | :--- | :--- |
| **SLOW (YAVAŞ)** | `1500 ms` | ~40 msg/min | 🟢 Very Safe | Recommended for large message histories to prevent rate limits. |
| **NORMAL** | `800 ms` | ~75 msg/min | 🟡 Balanced | Default setting, good balance between speed and stability. |
| **FAST (HIZLI)** | `400 ms` | ~150 msg/min | 🟠 Aggressive | High speed; may trigger occasional 429 rate-limit pauses. |
| **TURBO** | `150 ms` | ~400 msg/min | 🔴 Risky | Very fast; frequent rate limit throttling. |
| **MAX** | `0 ms` | Maximum | ⚠️ Extreme | No delay; highest rate-limit risk. Use with caution. |

---

## 📸 Interface Preview

```text
+-----------------------------------------------------------------------------------+
| DMCLEAR   Discord Mesaj Silici                                Made By Haribo      |
+-----------------------------------------------------------------------------------+
| [▶ SİLMEYİ BAŞLAT]  [⏸ DURAKLAT]  [⏹ DURDUR]   Status: Hazır                     |
+-----------------------------------------+-----------------------------------------+
| [Discord User Token]                    | Canlı İşlem Günlüğü (Live Console)      |
| [ ************************** ] [Bağlan] | [15:10:02] [INFO] DMCLEAR başlatıldı    |
| Durum: user#1234 olarak bağlandı        | [15:10:05] [SCAN] 50 mesaj tarandı      |
|                                         | [15:10:06] [DEL] Mesaj silindi (ID: ..) |
| [Hedef Kanal ID]                        | [15:10:07] [DEL] Mesaj silindi (ID: ..) |
| [ 123456789012345678 ] [Bilgi]          |                                         |
|                                         | İstatistikler                           |
| [DM Kanalları (Otomatik)]               | ┌──────────────┬──────────────┐         |
| [ DM Listesini Çek ]                    | │ Silinen:  42 │ Taranan: 100 │         |
| ┌─────────────────────────────────────┐ │ ├──────────────┼──────────────┤         |
| │ • Alice (ID: 111111111111111111)    │ │ │ Atlanan: 58 │ Limit:   0   │         |
| │ • Bob   (ID: 222222222222222222)    │ │ └──────────────┴──────────────┘         |
| └─────────────────────────────────────┘ |                                         |
|                                         | İlerleme: [████████████████░░░░] 42%    |
| [Filtreler]                             |                                         |
| Limit: [0     ]  İçerik: [         ]    |                                         |
| Gecikme: [800ms] [Slider: ======o=====] |                                         |
| Hız: [YAVAŞ] [NORMAL] [HIZLI] [TURBO]   |                                         |
+-----------------------------------------+-----------------------------------------+
```

---

## 🚀 Installation

### 1. Prerequisites
- **Python 3.8+** installed on your system.

### 2. Setup
Open your terminal / PowerShell in the tool directory:
```powershell
cd "C:\Users\Haribooo\Desktop\tool\dmclear"
```

Install the required library (`requests`):
```powershell
pip install -r requirements.txt
```

---

## 💻 Usage

### Quick Start (Windows)
Double-click [`run.bat`](file:///C:/Users/Haribooo/Desktop/tool/dmclear/run.bat) or run via terminal:
```powershell
python dmclear.py
```

### Step-by-Step Guide:
1. **Connect Account:**
   - Enter your Discord User Token into the token field.
   - Click **Bağlan (Connect)**. The app verifies the token and displays your Discord username.
2. **Select Channel:**
   - **Method A (DM List):** Click **DM Listesini Çek (Fetch DMs)** and select a contact from the list.
   - **Method B (Channel ID):** Paste any DM, Group DM, or Server Text Channel ID directly.
3. **Configure Options:**
   - **Limit:** Enter `0` to delete all your messages, or specify a number (e.g. `50`).
   - **Content Filter:** Enter text to only delete messages containing that keyword (optional).
   - **Speed / Delay:** Choose a speed preset (`NORMAL` 800ms is recommended).
4. **Start Deletion:**
   - Click the green **▶ SİLMEYİ BAŞLAT (Start Deletion)** button.
   - You can pause or stop the process at any time.

---

## 📂 Project Structure

```text
dmclear/
│
├── dmclear.py            # Main application with Tkinter GUI & purge engine
├── run.bat               # Windows batch launcher
├── requirements.txt      # Dependencies (requests)
└── README.md             # Project documentation
```

---

## 🛡️ Rate Limits & Safety

- **Discord Rate Limits (429):** Discord limits how many delete requests an account can perform in a given time window. If rate limited, DMCLEAR automatically catches the `retry_after` response and sleeps until safe.
- **Recommended Delay:** Keep the delay at **800ms or higher** for maximum account safety.
- **Account Safety:** Avoid using multiple cleaner tools at the same time.

---

## ⚖️ Disclaimer

This tool is provided for **educational, data management, and personal privacy purposes only**.
Automating user accounts (self-botting) violates Discord's Terms of Service. The author is not responsible for any account suspensions or consequences resulting from the use of this tool. Use at your own risk.
