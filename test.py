import discum #import discum for self bots
from time import sleep #for waiting
import json

bots = [] #array for discum bots
targets = [
    "1000",
    "2000",
    "3000",
    "4000",
    "5000",
    "6000",
    "7000",
    "8000",
    "9000",
    "0001",
    "0002",
    "0003",
    "0004",
    "0005",
    "0006",
    "0007",
    "0008",
    "0009",
    "1111",
    "2222",
    "3333",
    "4444",
    "5555",
    "6666",
    "7777",
    "8888",
    "9999",
    "1234",
    "6969",
    "0101"]

print("Reading accounts.txt...\n")
#open the accounts file (format = email:password:token)
with open("accounts.txt") as accountsFile:
    accounts = accountsFile.readlines()

#caclulate how long to sleep after begging
sleep_time = (60*60*2)/len(accounts)-5*len(accounts)

print("Logging into accounts...")
#log into each account
num = 1 #counter
for account in accounts:
    account = account.replace("\n","").split(":")
    #add the account as a discum client
    bots.append(discum.Client(token=account[2],password=account[1],log=False))
    print("Logged in on account #"+str(num)) #status message
    num += 1

lapse = 1
print("\nStarting... [sleep time is "+str(sleep_time)+"s]\n")
print("Starting lapse #1")
while True:
    num = 1 #counter

    for bot in bots: #repeat for each discord account
        old_data = None
        matching_discrims = None

        #try to send a message to get discrims from carl, try 3 times, worst case return a fake username
        matching_discrims = []
        for attempt in range(3):
            try:
                old_data = bot.sendMessage("884358136998285322", "?discrim").json()["author"]
                sleep(6)
                matching_discrims = bot.getMessages("884358136998285322",1).json()
                matching_discrims = matching_discrims[0]
                matching_discrims = matching_discrims["embeds"][0]["description"].split("\n")
                break
            except:
                print("Failed to get dyno embed. Trying again...")
                sleep(5)

        if len(matching_discrims) == 0:
            print("Finding dyno embed failed.")
            matching_discrims = ["Something went wrong#"+old_data["discriminator"]]
            success = False
            break
        
        #make sure the # is on the right (some languages make it go to the left)
        for matching_discrim in matching_discrims:
            if matching_discrim.startswith("#"):
                matching_discrims.remove(matching_discrim)
                continue
            if len(matching_discrim) < 10:
                matching_discrims.remove(matching_discrim)
                continue

        try:
            for matching_discrim in matching_discrims:
                try:
                    matching_discrim = matching_discrim[:matching_discrim.find("#")]

                    new_data = bot.setUsername(matching_discrim).json()
                    try:
                        if new_data["errors"]['username']['_errors'][0]['code'] == "USERNAME_RATE_LIMIT":
                            print("Hit ratelimit, moving on to next account...")
                            break
                    except:
                        pass
                    discrim = new_data["discriminator"]

                    print("Changed username of account #"+str(num)+" from \""+old_data["username"]+"\" to \""+matching_discrim+"\"")
                    print("Old discrim [#"+str(old_data["discrim"])+"] was changed to [#"+str(discrim)+"]")

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
                except:
                    print("Error. Trying again...")
                    continue

            if success:
                #increase counter and sleep
                sleep(sleep_time)
                num += 1
                success = None
            else:
                success = None
                continue


    print("\nLapse #"+str(lapse)+" complete.")