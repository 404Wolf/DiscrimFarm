from time import sleep
import json
import discum

#load a file in and return an array of line by line
def load(file):
    with open(file) as file:
        output = file.readlines()
        for item in output:
            output[output.index(item)] = item.replace("\n","")
    return output

def dump(file,item):
    with open(file,"a") as file:
        file.write("\n"+item)

blacklist = load("blacklist.txt") #array with blacklisted 
targets = load("blacklist.txt")
accounts = load("accounts.txt")

bots = [] #array for discum bots

#caclulate how long to sleep after begging
sleep_time = (60*60*2.1)/len(accounts)


# proxies = genProxies()
print("Logging into accounts...")
#log into each account
num = 1 #counter
for account in accounts:
    while True:
        try:
            account = account.split(":")

            bots.append(discum.Client(
                token=account[2],
                password=account[1],
                log=True))
                
            print("Logged in on account #"+str(num)) #status message
            num += 1
            break
        except:
            print("Error logging in.")
            break

lapse = 1 #lapse counter
print("\nStarting... [sleep time is "+str(round(sleep_time,3))+"s]\n")
print("Starting lapse #1")

while True:
    num = 1 #account counter

    for bot in bots: #repeat for each discord account
        old_data = None
        new_usernames = None

        #try to send a message to get discrims from carl, try 3 times, worst case return a fake username
        new_usernames = []
        for attempt in range(3):
            old_data = bot.sendMessage("884358136998285322", "?discrim").json()["author"]
            sleep(6)
            new_usernames = bot.getMessages("884358136998285322",1).json()
            new_usernames = new_usernames[0]
            new_usernames = new_usernames["embeds"][0]["description"].split("\n")
            break

        #if the dyno embed is null, change username to "something went wrong"
        if len(new_usernames) == 0:
            print("Finding dyno embed failed.")
            new_usernames = ["Something went wrong#0000"]
            break
        
        #make sure the # is on the right (some languages make it go to the left)
        for new_username in new_usernames:

            #flagging bad new usernames:
            def flag(username):
                blacklist.append(username)
                dump("blacklist.txt",username)
                new_usernames.remove(username)

            #remove username if it goes right to left
            if new_username.startswith("#"):
                print(f"Flagging {new_username} because it starts with a #.")
                flag(new_username)
                continue

            #remove username if it is too short
            if len(new_username) < 9:
                print(f"Flagging {new_username} because it is too short.")
                flag(new_username)
                continue

            #remove username if is the current username
            if new_username == old_data["username"]+"#"+old_data["discriminator"]:
                print(f"Flagging {new_username} because it matches the current username.")
                flag(new_username)
                continue
                
            #remove username if it's in the blacklist
            if new_username[:-5] in blacklist:
                print(f"Flagging {new_username} because it is in the blacklist")
                flag(new_username)
                continue

            for new_username in new_usernames:
                new_username = new_username[:new_username.find("#")]
                print("Attempting to change name to \""+new_username+"\"")
                new_data = bot.setUsername(new_username).json()

                try:
                    if new_data["errors"]['username']['_errors'][0]['code'] == "USERNAME_RATE_LIMIT":
                        print("Hit ratelimit, moving on to next account...")
                        break
                    elif new_data["errors"]['username']['_errors'][0]['code'] == "USERNAME_TOO_MANY_USERS":
                        blacklist.append(new_username)
                        dump("blacklist.txt",new_username)
                        sleep(5)
                        continue
                except KeyError:
                    pass

                discrim = new_data["discriminator"]

                print("Changed username of account #"+str(num)+" from \""+old_data["username"]+"\" to \""+new_username+"\"")
                print("Old discrim [#"+str(old_data["discriminator"])+"] was changed to [#"+str(discrim)+"]")

                #remove account from accounts file if success
                if discrim in targets:
                    with open("success.txt","a") as success_file:
                        success_file.write(str(new_data["token"])+"\n")
                    print("Success! Discrim \""+str(discrim)+"\" obtained!")
                    bot.sendMessage("884679723769286716","@everyone, my new discrim is #**"+str(discrim)+"**!")
                    for account in accounts:
                        if new_data["token"] in account:
                            accounts.remove(account)
                    new_accounts = ""
                    with open("accounts.txt","w") as accounts_file:
                        for account in accounts:
                            new_accounts += account.replace("\n","")+"\n"
                        accounts_file.write(new_accounts[:-1])
                    bots.remove(bot)
                else:
                    print("New discrim not in targets!")
                break

            num += 1
            sleep(sleep_time)
            break
            
    print("\nLapse #"+str(lapse)+" complete.")