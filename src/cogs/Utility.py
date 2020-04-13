######### Bot V0.2.1 created by Kiran Wallace #########
### NOTE: This is not the main module. Please run main.py
# This is an extension of main.py
# This bot is for the intent to be used as a fun resource for Discord servers and is a work in progress
#
# In this section of code, you will find the following:
### Commands:
# .ping, .clear, .changestatus
### Functions:
# setup
################################################################################################################

import discord
import random
from main import ConsoleMessage, ErrorLog, add_usage
from discord.ext import commands

class Utility(commands.Cog):
    #initialises object with client from main
    def __init__(self, client):
        self.client = client

########################################################################################################
#############################################   COMMANDS   #############################################
#This section is for command calling, all functions with the decorator @client.command() will be called
#if typed into discord with the prefix '.'

    #simply sends a message "pong" with the latency between the server and client in milliseconds
    #not massivly useful, just interesting
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong! {round(self.client.latency * 1000)}ms')
        add_usage("pings")

    #clean up tool that deletes a specified amount of messages, default 1
    #must have admin privileges to use
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

        #informs the console of the changes and adds to clear counter in "usage.json"
        if amount > 1:
            ConsoleMessage(f'{ctx.author} cleared {amount} messages from channel #{ctx.channel.name}')
            add_usage("messages cleared",amount)
        elif amount == 1:
            ConsoleMessage(f'{ctx.author} cleared 1 message from channel #{ctx.channel.name}')
            add_usage("messages cleared")

    #if an error is thrown for using .clear
    @clear.error
    async def clear_error(self, ctx, error):
        #if the user does not have the required permissions, inform the console
        if isinstance(error, commands.CheckFailure):
            ConsoleMessage(f'{ctx.author} failed to use .clear due to lack of privileges')
        #otherwise, assume poor input
        else:
            randval = random.randint(2,20)
            await ctx.send(f'Sorry {ctx.author.mention}, I don\'t think I understand. Try `.clear {randval}` to remove {randval} messages')

    #changes the status of the bot on discord below the bots name. The user can choose from either "playing", "watching" or "listening to"
    #must have admin privileges to use
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changestatus(self, ctx, statType, *, status):
        #creates the action that the bot is doing based on input
        if statType.lower() == 'watching':
            customAct = discord.Activity(type=discord.ActivityType.watching, name = status)
        elif statType.lower() == 'listening':
            customAct = discord.Activity(type=discord.ActivityType.listening, name = status)
        elif statType.lower() == 'playing':
            customAct = discord.Game(status)

        #if the inputted action is not on the valid list, inform user and give valid examples
        else:
            await ctx.send(f'Sorry {ctx.author.mention}, but I need to be playing, watching or listening to something\nE.g: `.changestatus playing Mario` means that I can play Mario! :smile:')
            return

        #changes the status of the bot
        await self.client.change_presence(status=discord.Status.idle, activity=customAct)

        #informs the console of the change and adds data to "usage.json"
        ConsoleMessage(f'{ctx.author} changed the status to {statType} {status}')
        add_usage("status changes")

    #upon error for .changestatus
    @changestatus.error
    async def changestatus_error(self, ctx, error):
        #if the error is due to lack of privileges, inform console
        if isinstance(error, commands.CheckFailure):
            ConsoleMessage(f'{ctx.author} failed to use .changestatus due to lack of privileges')
        #otherwise, add errorlog
        else:
            ErrorLog(error)

#adds extension to client when called
def setup(client):
    client.add_cog(Utility(client))
