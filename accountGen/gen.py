import asyncio
from pyppeteer import launch
from random import sample,randint,choice
import pyperclip

async def main():
    browser = await launch(headless=False) #launch a headed browser
    mail_site = await browser.newPage() #make a new tab for mail.tm

    async def getEmail():
        
        await mail_site.goto("https://mail.tm",waitUntil="load") #go to the url
        await asyncio.sleep(6)

        for x in range(9):
            await mail_site.keyboard.press(key='Tab')
            await asyncio.sleep(.1)
        #copy box text
        await mail_site.keyboard.down(key='Control')
        await mail_site.keyboard.down(key='C')
        await mail_site.keyboard.up(key='Control')
        await mail_site.keyboard.up(key='C')
        return pyperclip.paste()

    #generate email and password
    email = await getEmail()
    password = "".join(sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",14))
    month = choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    year = str(randint(1990,2001))
    day = str(randint(1,25))
    
    #go to discord
    discord_site = await browser.newPage() #make a new tab for discord
    await discord_site.goto("https://discord.com/register",waitUntil='networkidle2') #go to discord's register page

    #fill in the input boxes
    email_box = await discord_site.waitForXPath("//input[@name='email']")
    await email_box.type(email)
    name_box = await discord_site.waitForXPath("//input[@name='username']")
    await name_box.type("null")
    password_box = await discord_site.waitForXPath("//input[@name='password']")
    await password_box.type(password)

    #use keyboard input to choose DOB
    await discord_site.keyboard.press(key='Tab')
    await asyncio.sleep(.1)
    await discord_site.keyboard.type(month)
    await discord_site.keyboard.press(key='Tab')
    await asyncio.sleep(.1)
    await discord_site.keyboard.type(day)
    await discord_site.keyboard.press(key='Tab')
    await asyncio.sleep(.1)
    await discord_site.keyboard.type(year)
    await asyncio.sleep(.1)
    await discord_site.keyboard.press(key='Tab')
    await asyncio.sleep(.1)
    await discord_site.keyboard.press(key='Enter')
    input("Click enter when you've finished solving the captcha, and adding phone verification.")

    email_url = await mail_site.evaluate('document.documentElement.outerHTML',force_expr=True)
    email_url = email_url[email_url.find("""<li><a href="/en/view/"""):]
    email_url = email_url[13:email_url.find("""/" class=""")]
    email_url = "https://mail.tm/"+email_url
    await mail_site.goto(email_url)

    content = await mail_site.evaluate("""() => new XMLSerializer().serializeToString(document)""")
    with open("test.txt","w",encoding="utf-8") as test:
        test.write(str(content))
    await asyncio.sleep(500)

#     await discord_site.evaluate("""() => {
#   localStorage.getItem('token');
#     })""")
    

asyncio.get_event_loop().run_until_complete(main())

#await browser.close() #close browser