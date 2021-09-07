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
for account in [accounts[0]]:
    account = account.replace("\n","").split(":")
    #add the account as a discum client
    bots.append(discum.Client(token=account[2],password=account[1],log=False))
    print("Logged in on account #"+str(num)) #status message
    num += 1

bot = bots[0]