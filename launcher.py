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
                                    "message": "๐ ๐ ๐ ๐ ๐ ๐ ๐ ๐คฃ ๐ ๐ ๐ ๐ ๐ โบ ๐ ๐ ๐ ๐ฅฐ ๐ ๐ ๐ ๐ ๐ฅฒ ๐คช ๐ ๐ ๐ ๐ค ๐ ๐ค ๐ฅธ ๐ง ๐ค  ๐ฅณ ๐ค ๐คก ๐ ๐ถ ๐ ๐ ๐ ๐ ๐คจ ๐ค ๐คซ ๐คญ ๐คฅ ๐ณ ๐ ๐ ๐  ๐ก ๐คฌ ๐ ๐ ๐ โน ๐ฌ ๐ฅบ ๐ฃ ๐ ๐ซ ๐ฉ ๐ฅฑ ๐ค ๐ฎโ๐จ ๐ฎ ๐ฑ ๐จ ๐ฐ ๐ฏ ๐ฆ ๐ง ๐ข ๐ฅ ๐ช ๐คค ๐ ๐ญ ๐คฉ ๐ต ๐ตโ๐ซ ๐ฅด ๐ฒ ๐คฏ ๐ค ๐ท ๐ค ๐ค ๐คฎ ๐คข ๐คง ๐ฅต ๐ฅถ ๐ถโ๐ซ๏ธ ๐ด ๐ค ๐ ๐ฟ ๐น ๐บ ๐ฉ ๐ป ๐ โ  ๐ฝ ๐ค ๐ ๐บ ๐ธ ๐น ๐ป ๐ผ ๐ฝ ๐ ๐ฟ ๐พ ๐ ๐คฒ ๐ ๐ ๐ ๐ค ๐ ๐ ๐ โ ๐ค ๐ค ๐ค โ ๐ค ๐ค ๐ ๐ค ๐ค ๐ ๐ ๐ ๐ โ โ ๐ค ๐ ๐ ๐ ๐ค ๐ช ๐ฆพ ๐ โ ๐คณ ๐ ๐ฆต ๐ฆฟ ๐ฆถ ๐ ๐ฆท ๐ ๐ ๐ฆป ๐ ๐ ๐ ๐ง  ๐ซ ๐ซ ๐ฆด ๐ค ๐ฅ ๐ฃ ๐ซ ๐ถ ๐ง ๐ง ๐ฆ ๐ฉ ๐ง ๐จ ๐ฉโ๐ฆฑ ๐งโ๐ฆฑ ๐จโ๐ฆฑ ๐ฉโ๐ฆฐ ๐งโ๐ฆฐ ๐จโ๐ฆฐ ๐ฑโโ๏ธ ๐ฑ " + str(
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
