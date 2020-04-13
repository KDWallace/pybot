######### Bot V0.2.1 created by Kiran Wallace #########
#### - created 8th April 2020 - last edit 13th April
#
######### API Created by Rapptz on GitHub #########
#https://github.com/Rapptz/discord.py
# This bot is for the intent to be used as a fun resource for Discord servers and is a work in progress
#
# In this section of code, you will find the following:
### Events:
# on_ready, on_command_error, on_member_join, on_member_remove
### Commands:
# .load, .unload, .reload
### Functions:
# add_usage, ConsoleMessage, ErrorLog, has_channel_perms
################################################################################################################

import discord
import os
import json
from datetime import datetime
from discord.ext import commands

#generated token that allows access to your bot
#https://discordapp.com/developers/applications/
#select your application/bot and click "Bot" on the left hand side
#you will find your Token under the Bots username
#if the token is given out unintentionally, simply regenerate your Token

### Do not share your token! This could grant anyone access to your bot ###
TOKEN = ''
#prefix needed before a command is called
#(Changing this may make a few things not make sense as the bot will tell you to use '.' in some of its messages. It will work though)
client = commands.Bot(command_prefix = '.')
#directory for the bot
PATH = (os.path.dirname(os.path.realpath(__file__)))[:-4]

#function for adding stats to "usage.json" for future "stat" update.
def add_usage(use,add=1):
    #will attempt to find and open "usage.json"
    try:
        with open(f'{PATH}\\data\\usage.json','r') as f:
            stats = json.load(f)
        #will attempt to add to existing stat from the json file
        try:
            stats[use] += add
        #upon failing, assume stat does not exist yet and create a new one
        except:
            stats[use] = add
        #overwrites the file with the new usage data
        with open(f'{PATH}\\data\\usage.json','w') as f:
            json.dump(stats, f, indent=4)
    #upon failing, will create a new dictionary with the data to add and create a new file called "usage.json"
    except:
        stats = {}
        stats[use] = add
        with open(f'{PATH}\\data\\usage.json','w') as f:
            json.dump(stats, f, indent=4)

#function for printing to the console and appending data to "../data/user logs/"
def ConsoleMessage(message):
    #formatting for the console with the time, a separator and the message
    message = f'{datetime.now().strftime("%H:%M:%S")}¦ {message}'
    #appends to existing or creates a new file with date formatting. If one does not exist for that day then will create a new log
    with open(f'{PATH}\\data\\user logs\\{datetime.today().strftime("%d-%m-%Y")}.txt','a') as f:
        f.write(message + '\n')
    print(message)

#very similar to ConsoleMessage(message) above
#function for printing a warning on the console and appending data to "../data/error logs/", bug fixing purposes
def ErrorLog(error):
    #adds to "Errors caught" stat in "usage.json"
    add_usage("Errors caught")
    #formatting for the console with the time, a separator and the message
    message = f'{datetime.now().strftime("%H:%M:%S")}¦ '
    #appends to existing or creates a new file with date formatting. If one does not exist for that day then will create a new log
    with open(f'{PATH}\\data\\error logs\\{datetime.today().strftime("%d-%m-%Y")}.txt','a') as f:
        f.write(f'{message}{error}\n')
    print(f'{message}== An error occured == Please see the updated error logs at ..\\data\\error logs\\{datetime.today().strftime("%d-%m-%Y")}.txt')

#function for checking if the command in question can be used in the current server channel/category
def has_channel_perms(ctx):
    #opens location for the json with the command permissions data
    with open(f'{PATH}\\config\\command locations.json', 'r') as f:
        cmds = json.load(f)
    #cycles through all of the commands that are found in the json until the command in question is found
    for command in cmds["commands"]:
        if ctx.message.content.startswith(command["name"]):
            #if the whitelist is enabled, only channels/categorys found in the whitelists are permitted to use the command
            if command["whitelist"]:
                #searches permitted channels for channel command was used in, if found will return true
                for channel in command["whitelist channels"]:
                    if ctx.channel.id == channel["id"]:
                        return True
                #searches permitted categorys for category command was used in, if found will return true
                for category in command["whitelist category"]:
                    if ctx.channel.category_id == category["id"]:
                        return True
                #if current channel/category was not found in either list and "whitelist" is active, assume not permitted and return false
                return False
            #if the whitelist is not enabled but blacklist is enabled, channels/categorys found in these lists are not permitted to use the command but all others are
            elif command["blacklist"]:
                #searches non-permitted channels for channel command was used in, if found will return false
                for channel in command["blacklist channels"]:
                    if ctx.channel.id == channel["id"]:
                        return False
                #searches non-permitted categorys for category command was used in, if found will return false
                for category in command["blacklist category"]:
                    if ctx.channel.category_id == category["id"]:
                        return False
                #if current channel/category was not found in either list and "blacklist" is active, assume permitted and return true
                return True
            break
    #if command is not found or there is no whitelist and blacklist enabled, assume has permissions
    return True

######################################################################################################
#############################################   EVENTS   #############################################
#This section is for event checking and will call the below functions if the event in question occures

#function called if the bot successfully boots up and is ready for use
@client.event
async def on_ready():
    #will load all extensions of the bot that can be found in the dir ./cogs
    #cogs allow for commands to be split into sections to make fixing easier and allows for the unloading/reloading of said sections
    for filename in os.listdir('./cogs'):
        #extensions are only considered if it is a python program (.py suffix)
        if filename.endswith('.py'):
            print(f'        Loading extension: {filename[:-3]}...',end='')
            client.load_extension(f'cogs.{filename[:-3]}')
            print('Complete')
    #once all extensions are loaded, host is informed that the bot is active
    print(f'   - {client.user.name} is online!')
    print(' ------------------------------------------------------------------')
    #adds to "Successful bootups" stat in "usage.json"
    #originally for testing the add_usage() function but was kept for fun
    add_usage("Successful bootups")

#function for informing what to do if a command throws an error, prevents spam in the console
@client.event
async def on_command_error(ctx,error):
    #ignores invalid input
    if isinstance(error, commands.CommandNotFound):
        pass
    #otherwise, will display a small warning in the console and post the error in "../data/error logs/"
    else:
        ErrorLog(error)

#Event for member joining the server
@client.event
async def on_member_join(member):
    ConsoleMessage(f'{member} has joined the server')

#Event for error leaving the server
@client.event
async def on_member_remove(member):
    ConsoleMessage(f'{member} has left the server')


########################################################################################################
#############################################   COMMANDS   #############################################
#This section is for command calling, all functions with the decorator @client.command() will be called
#if typed into discord with the prefix '.'

#function for loading and enabling extensions from ./cogs
#used for if new extension has been made or a previous one was unloaded/failed to load
#must have admin permissions
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    print(f'        ¦ Loading extension: {extension}...',end='')
    client.load_extension(f'cogs.{extension}')
    print('Complete')
    ConsoleMessage(f'{ctx.author} loaded extension {extension}')
    await ctx.send(f'Extension {extension} has been enabled along with all of its associated commands.\nTo see avaliable commands, type `.help`')

#called upon error for .load
@load.error
async def load_error(ctx, error):
    #if the user does not have the appropriate permissions
    if isinstance(error, commands.CheckFailure):
        ConsoleMessage(f'{ctx.author} failed to use .load due to lack of privileges')
    #otherwise, add to error log
    else:
        ErrorLog(error)

#function for unloading and disabling extensions from ./cogs
#used if admin user wants to prevent usage of certain commands
#must have admin permissions
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    print(f'        ¦ Unloading extension: {extension}...',end='')
    client.unload_extension(f'cogs.{extension}')
    print('Complete')
    ConsoleMessage(f'{ctx.author} unloaded extension {extension}')
    await ctx.send(f'Extension {extension} has been disabled along with all of its associated commands.\nTo see avaliable commands, type `.help`')

#called upon error for .unload
@unload.error
async def unload_error(ctx, error):
    #if the user does not have the appropriate permissions
    if isinstance(error, commands.CheckFailure):
        ConsoleMessage(f'{ctx.author} failed to use .unload due to lack of privileges')
    #otherwise, add to error log
    else:
        ErrorLog(error)

#function for unloading and then loading extensions from ./cogs
#used for changing the code of an extension (mostly in "feature" fixing or adding features) and wanting to apply without closing the client
#must have admin permissions
@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    print(f'        ¦ Reloading extension: {extension}...',end='')
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Complete\n        ¦ Extension {extension} reloaded')
    ConsoleMessage(f'{ctx.author} reloaded extension {extension}')
    await ctx.send(f'Extension {extension} has been reloaded along with all of its associated commands.\nTo see avaliable commands, type `.help`')

#called upon error for .reload
@reload.error
async def reload_error(ctx, error):
    #if the user does not have the appropriate permissions
    if isinstance(error, commands.CheckFailure):
        ConsoleMessage(f'{ctx.author} failed to use .reload due to lack of privileges')
    #otherwise, add to error log
    else:
        ErrorLog(error)
        await ctx.send(f'Extension has failed to reload. If the extension has been unloaded, try `.load` instead. Make sure it\'s an existing extension\n(Note: This is for code fixing without closing the client, you don\'t need to use this unless you know what you\'re doing)')

#if this program is called __main__ by the interperator, run the client
if __name__ == '__main__':
    print(' =========================== PyBot V0.2 =========================== ')
    print(f'   - Booted at {datetime.now().strftime("%H:%M:%S")}\n   - Please wait...')
    client.run(TOKEN)
