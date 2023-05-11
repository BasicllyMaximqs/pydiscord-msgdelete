import requests
import json

import random
import time
token = ""

discord_main = "https://discord.com/api/v9/users/@me"

hd = {"Authorization": token}

identifier_no = 0

def init():
    if len(token) < 1:
        print("Empty Token, exiting")
        exit()
    global identifier_no
    print("Exporting Information..")
    request_discord_main = requests.get(discord_main, headers=hd)
    print("API Call returned " + str(request_discord_main.status_code))
    formatted_utf_request = json.loads(request_discord_main._content.decode("utf-8"))
    identifier_no = formatted_utf_request['id']
    print(f"Detected User: '{formatted_utf_request['username']}#{formatted_utf_request['discriminator']}' (ID: "+identifier_no+")")



    request_discord_channel = requests.get(discord_main + "/channels", headers=hd)
    
    formatted_channel_request = json.loads(request_discord_channel._content.decode("utf-8"))
    print("\nDumping Direct Message Channels")

    for item in formatted_channel_request:
        print("********************")
        print("CHANNEL ID " + item["id"])
        for it in item["recipients"]:
            print(it["username"] + "#" + it["discriminator"])

    channel_id_input = input("\ninput channel id:")

    limit = 50
    loops = 5
    last_message_id = 0 # dont change

    add_delay_per_idx = False
    idx_delay = 2 #seconds after new page

    add_missmatch_debug_msg = False

    for i in range(1, loops+1):
        print("\n\nBeginning Loop #"+str(i))
        if add_delay_per_idx:
            print("Index Delay Sleeping for " + str(idx_delay) + "s...")
            time.sleep(idx_delay)
        opt_string = ""
        if (last_message_id != 0):
            opt_string = "before=" + str(last_message_id) + "&"
        channel_messages_fetch = requests.get("https://discord.com/api/v9/channels/" + str(channel_id_input) + "/messages?" + opt_string +"limit=" + str(limit), headers=hd)

        formatted_messages_fetch = json.loads(channel_messages_fetch._content.decode("utf-8"))
        print("[ Loop #"+str(i)+"] Fetching the last " + str(limit) + " messages from Channel-ID: " + channel_id_input)
        print("URL: " + channel_messages_fetch.url)
        rateLimit = False



        message_count = 0

        for item in formatted_messages_fetch:
            last_message_id = int(item["id"])
            if (item["author"]["id"] != identifier_no):
                if add_missmatch_debug_msg:
                    print("Message Missmatch [ID: "+item["author"]["id"]+"], Expected " + identifier_no)
                continue
            
            print("\n[ Loop #"+str(i)+" | Item #"+str(message_count)+" ] New Item ID " + item["id"] + " ||| Content: " + item["content"] + " |=| by " + item["author"]["username"])
            print("[ Loop #"+str(i)+" | Item #"+str(message_count)+" ] Sending Request to Delete " + item["id"])
            if rateLimit:
                print("[ Loop #"+str(i)+"] Ratelimit Sleeping..")
                time.sleep(random.randint(3,7))
                rateLimit = False
            attempt = requests.delete("https://discord.com/api/v9/channels/" + str(channel_id_input) + "/messages/" + item["id"], headers=hd)

            if (attempt.status_code == 429):
                rateLimit = True

            print("[ Loop #"+str(i)+" | Item #"+str(message_count)+" ] Deletion returned " + str(attempt.status_code))
            message_count += 1
            




init()


