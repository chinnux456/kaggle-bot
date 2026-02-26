#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════════════════════════
 KAGGLE BOT - SAFE AUTOMATED RUNNER
 ✅ Anti-Sleep | ✅ Anti-Disconnect | ✅ 11 Hour Runtime | ✅ Auto-Shutdown
════════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import time
import signal
import threading
import subprocess
import re
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION - CHANGE YOUR GOOGLE DRIVE FILE ID HERE
# ══════════════════════════════════════════════════════════════════════════════
SCRIPT_FILE_ID = "YOUR_GOOGLE_DRIVE_FILE_ID_HERE"  # ← CHANGE THIS
MAX_RUNTIME_HOURS = 11
MAX_RUNTIME_SECONDS = MAX_RUNTIME_HOURS * 60 * 60
START_TIME = time.time()

# ══════════════════════════════════════════════════════════════════════════════
#  STARTUP BANNER
# ══════════════════════════════════════════════════════════════════════════════
print()
print("═" * 70)
print("  🤖 KAGGLE BOT - AUTOMATED RUNNER")
print("═" * 70)
print(f"  📅 Start Time      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"  ⏰ Max Runtime     : {MAX_RUNTIME_HOURS} hours")
print(f"  🛑 Auto-Stop At    : {(datetime.now() + timedelta(hours=MAX_RUNTIME_HOURS)).strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"  💻 Platform        : Kaggle (4 CPU, 30GB RAM)")
print("═" * 70)
print()

# ══════════════════════════════════════════════════════════════════════════════
#  ANTI-SLEEP / KEEP-ALIVE SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
class KeepAliveSystem:
    """Prevents Kaggle from disconnecting due to inactivity"""
    
    def __init__(self):
        self.running = True
        self.thread = None
        self.ping_count = 0
    
    def _keep_alive_loop(self):
        while self.running:
            elapsed = time.time() - START_TIME
            remaining = MAX_RUNTIME_SECONDS - elapsed
            
            if remaining <= 0:
                print("\n⏰ 11 hours reached! Shutting down gracefully...")
                self.running = False
                os._exit(0)
                break
            
            self.ping_count += 1
            
            # Print status every 30 minutes
            if self.ping_count % 30 == 0:
                elapsed_hrs = int(elapsed // 3600)
                elapsed_mins = int((elapsed % 3600) // 60)
                remaining_hrs = int(remaining // 3600)
                remaining_mins = int((remaining % 3600) // 60)
                print(f"💓 Keep-Alive | Elapsed: {elapsed_hrs}h {elapsed_mins}m | Remaining: {remaining_hrs}h {remaining_mins}m")
            
            # CPU activity to prevent idle
            _ = sum(range(10000))
            time.sleep(60)
    
    def start(self):
        self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
        self.thread.start()
        print("✅ Anti-Sleep system: ACTIVATED")
        print("✅ Auto-Shutdown timer: ACTIVATED (11 hours)")
        print()
    
    def stop(self):
        self.running = False
        print("🛑 Keep-Alive system: STOPPED")

# Start keep-alive
keep_alive = KeepAliveSystem()
keep_alive.start()

# ══════════════════════════════════════════════════════════════════════════════
#  SHUTDOWN HANDLERS
# ══════════════════════════════════════════════════════════════════════════════
def graceful_shutdown(signum, frame):
    print("\n🛑 Shutdown signal received. Exiting...")
    keep_alive.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1: INSTALL DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
print("📦 Step 1: Installing dependencies...")
os.system("pip install gdown requests --quiet 2>/dev/null")
print("✅ Done!")
print()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2: DOWNLOAD SCRIPT FROM GOOGLE DRIVE
# ══════════════════════════════════════════════════════════════════════════════
print("📥 Step 2: Downloading my_script.py from Google Drive...")

if os.path.exists("my_script.py"):
    os.remove("my_script.py")

result = subprocess.run(
    ["gdown", SCRIPT_FILE_ID, "-O", "my_script.py"],
    capture_output=True,
    text=True
)

if os.path.exists("my_script.py"):
    file_size = os.path.getsize("my_script.py")
    print(f"✅ Downloaded! Size: {file_size:,} bytes")
else:
    print("❌ Download FAILED!")
    print(f"Error: {result.stderr}")
    sys.exit(1)
print()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3: CLEAR TELEGRAM CONFLICTS
# ══════════════════════════════════════════════════════════════════════════════
print("🔄 Step 3: Clearing Telegram conflicts...")

import requests

try:
    with open('my_script.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    token_match = re.search(r'TELEGRAM_BOT_TOKEN\s*=\s*["\']([^"\']+)["\']', content)
    
    if token_match:
        bot_token = token_match.group(1)
        try:
            requests.get(f"https://api.telegram.org/bot{bot_token}/deleteWebhook", timeout=10)
            requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1", timeout=10)
            time.sleep(2)
            print("✅ Telegram cleared!")
        except:
            print("⚠️ Could not clear Telegram")
    else:
        print("ℹ️ No Telegram token found, skipping")
except Exception as e:
    print(f"⚠️ Warning: {e}")
print()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4: RUN THE SCRIPT
# ══════════════════════════════════════════════════════════════════════════════
print("═" * 70)
print("  🚀 STARTING YOUR BOT")
print("═" * 70)
print()

MAX_RESTARTS = 5
restart_count = 0

while restart_count < MAX_RESTARTS:
    elapsed = time.time() - START_TIME
    remaining = MAX_RUNTIME_SECONDS - elapsed
    
    if remaining <= 60:
        print("\n⏰ Time limit reached. Stopping.")
        break
    
    try:
        exec(open("my_script.py", encoding='utf-8').read())
        break
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted")
        break
        
    except SystemExit as e:
        if e.code == 0:
            break
        restart_count += 1
        
    except Exception as e:
        restart_count += 1
        print(f"\n❌ Error: {e}")
        print(f"🔄 Restart {restart_count}/{MAX_RESTARTS} in 30s...")
        time.sleep(30)

# ══════════════════════════════════════════════════════════════════════════════
#  FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
total_runtime = time.time() - START_TIME
hours = int(total_runtime // 3600)
mins = int((total_runtime % 3600) // 60)

print()
print("═" * 70)
print("  ✅ SESSION COMPLETED")
print(f"  ⏱️ Runtime: {hours}h {mins}m")
print("═" * 70)

keep_alive.stop()
