from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import time
from threading import Thread
import config

DEBUG = True  # Enable or disable printing debug information to terminal
MESSAGES_DELAY = 0.05  # Time to wait after spam message sent
START_RAID_AFTER_CERTAIN_MESSAGE = False  # Start raid only after sending a message like "@bot_nick start" to chat

def gen_start_message(bots):
    message_final = ""
    for i in bots:
        message_final += f"@public{i[1]} start "
    return message_final 


def raid(chat_id, curr_vk_session):
    while True:
        curr_vk_session.method("messages.send", {"peer_id": chat_id,
                                    "message": "😀 😃 😄 😁 😆 😅 😂 🤣 😇 😉 😊 🙂 🙃 ☺ 😋 😌 😍 🥰 😘 😗 😙 😚 🥲 🤪 😜 😝 😛 🤑 😎 🤓 🥸 🧐 🤠 🥳 🤗 🤡 😏 😶 😐 😑 😒 🙄 🤨 🤔 🤫 🤭 🤥 😳 😞 😟 😠 😡 🤬 😔 😕 🙁 ☹ 😬 🥺 😣 😖 😫 😩 🥱 😤 😮‍💨 😮 😱 😨 😰 😯 😦 😧 😢 😥 😪 🤤 😓 😭 🤩 😵 😵‍💫 🥴 😲 🤯 🤐 😷 🤕 🤒 🤮 🤢 🤧 🥵 🥶 😶‍🌫️ 😴 💤 😈 👿 👹 👺 💩 👻 💀 ☠ 👽 🤖 🎃 😺 😸 😹 😻 😼 😽 🙀 😿 😾 👐 🤲 🙌 👏 🙏 🤝 👍 👎 👊 ✊ 🤛 🤜 🤞 ✌ 🤘 🤟 👌 🤌 🤏 👈 👉 👆 👇 ☝ ✋ 🤚 🖐 🖖 👋 🤙 💪 🦾 🖕 ✍ 🤳 💅 🦵 🦿 🦶 👄 🦷 👅 👂 🦻 👃 👁 👀 🧠 🫀 🫁 🦴 👤 👥 🗣 🫂 👶 👧 🧒 👦 👩 🧑 👨 👩‍🦱 🧑‍🦱 👨‍🦱 👩‍🦰 🧑‍🦰 👨‍🦰 👱‍♀️ 👱 " + str(
                                        random.randint(0, 163664527287)),
                                    "random_id": 0})
        time.sleep(MESSAGES_DELAY)

def spawn_bot(API_TOKEN, GROUP_ID):
    vk = vk_api.VkApi(token=API_TOKEN)
    vk._auth_token()
    vk.get_api()


    longpoll = VkBotLongPoll(vk, GROUP_ID)

    if DEBUG: print(f"Bot {GROUP_ID} Started")
    while True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.peer_id != event.object.from_id:
                    if START_RAID_AFTER_CERTAIN_MESSAGE and "start" in event.object.text:
                        th = Thread(target=raid, args=(event.object.peer_id, ))
                        th.start()
                    else:
                        th = Thread(target=raid, args=(event.object.peer_id, vk, ))
                        th.start()
    

bots = config.bots
print(gen_start_message(bots))
for i in bots:
    print("Starting BOT with ID: ", i[1])
    th = Thread(target=spawn_bot, args=(i[0], i[1], )).start()
    #print("Key: ", i[0])
