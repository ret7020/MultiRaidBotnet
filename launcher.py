from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import time
from threading import Thread
import config

DEBUG = True  # Enable or disable printing debug information to terminal
MESSAGES_DELAY = 0.05  # Time to wait after spam message sent
START_RAID_AFTER_CERTAIN_MESSAGE = True  # Start raid only after sending a message like "@bot_nick start" to chat
PREFIX_MESSAGE = "test prefix"
SENDER_ACCEPTED_ID = 1


with open("text.txt") as fd:
    TEXT = fd.readlines()

SET_LENGTH = len(TEXT)
def gen_start_message(bots):
    message_final = ""
    for i in bots:
        message_final += f"@public{i[1]} start "
    return message_final 


def raid(chat_id, curr_vk_session, bot_id):
    global stopped_bots, stop_event
    print("Started")
    msg_index = bot_id
    while not stop_event:
        print(bot_id, msg_index)
        curr_vk_session.method("messages.send", {"peer_id": chat_id,
                                    "message": f"{PREFIX_MESSAGE} {TEXT[msg_index]}",
                                    "random_id": 0})
        time.sleep(MESSAGES_DELAY)
        msg_index += bot_id + 1
        if SET_LENGTH <= msg_index:
            msg_index = 0
    stopped_bots += 1


stop_event = False
stopped_bots = 0
def spawn_bot(API_TOKEN, GROUP_ID, bot_id):
    global stopped_bots, stop_event
    vk = vk_api.VkApi(token=API_TOKEN)
    vk._auth_token()
    vk.get_api()

    longpoll = VkBotLongPoll(vk, GROUP_ID)
    if DEBUG: print(f"Bot {GROUP_ID} Started")
    while True:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message["peer_id"] != event.object.message["from_id"]:
                    if event.object.message["from_id"] == SENDER_ACCEPTED_ID:
                        cmd = event.object.message["text"].replace(f"[club{GROUP_ID}|@public{GROUP_ID}]", "").strip()
                        if "start" in cmd: # in event.object.message["text"]:
                            th = Thread(target=raid, args=(event.object.message["peer_id"], vk, bot_id ))
                            th.start()
                        elif cmd == "/":
                            vk.method("messages.send", {"peer_id": event.object.message["peer_id"], "message": '''Команды ботнета:
                                    start - запуск
                                    stop - остановка''', "random_id": 0})
                        elif cmd in ["stop", "/stop"]:
                            stopped_bots = 0
                            stop_event = True
                            print("Waiting for bots to stop...")
                            vk.method("messages.send", {"peer_id": event.object.message["peer_id"], "message": '''Бот остановлен''', "random_id": 0})
                            while stopped_bots < len(config.bots):
                                pass
                            print("All bots stoppped!")
                            stop_event = False

bots = config.bots
print(gen_start_message(bots))
index = 0
for i in bots:
    index += 1
    print("Starting BOT with ID: ", i[1])
    th = Thread(target=spawn_bot, args=(i[0], i[1], index, )).start()
