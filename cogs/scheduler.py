'''
Created on May 25, 2017

@author: mommo
'''
from discord.ext import commands


class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.dm_ids = ["187421759484592128", "174568535731732480", "178247686577848321", "162718986763632641", "266359719663239179"]
        self.games = []
    
    async def on_message(self, message):
        if not message.server.id == "211219033658228739": return #only listen to Discord & Dragons
        for g in self.games:
            if message.channel.id == g['planchan'].id:
                if message.author == g['dm'] and message.content == '--': # ends games
                    self.games.remove(g)
                    await self.bot.delete_channel(message.channel)
                    await self.bot.send_message(message.author, "Planning ended! Final player list: {}\nPingstring: {}".format(", ".join(p.mention for p in g['players']), " ".join("@" + str(p) for p in g['players'])))
                if message.content == '+': # joins game
                    if message.author in g['players']: await self.bot.send_message(message.author, "You are already the game DMed by {}.".format(g['dm'].mention))
                    elif len(g['players']) < g['maxp']: 
                        g['players'].add(message.author)
                        await self.bot.edit_message(g['plistmsg'], "Player List: " + ", ".join(p.mention for p in g['players']))
                        await self.bot.send_message(message.author, "You have been added to the game DMed by {}. Type `-` in the planning channel to drop out.".format(g['dm'].mention))
                    else:
                        await self.bot.send_message(message.author, "Sorry, that game is full.")
                if message.content == '-': # leaves game
                    if message.author in g['players']:
                        g['players'].remove(message.author)
                        await self.bot.edit_message(g['plistmsg'], "Player List: " + ", ".join(p.mention for p in g['players']))
                        await self.bot.send_message(message.author, "You have been removed from the game DMed by {}.".format(g['dm'].mention)) 
                    else:
                        await self.bot.send_message(message.author, "You cannot leave a game you aren't in.")
                if not message.author == g['dm']: await self.bot.delete_message(message)
    
    @commands.command(pass_context=True)
    async def startgame(self, ctx, max_players:int=6, *, desc="No description."):
        """Starts a game. Type `--` in the planning channel to end planning.
        max_players - The maximum number of players.
        desc - Info that is pinned."""
        if not ctx.message.author.id in self.dm_ids: return await self.bot.say("You are not a Dragon's Wake DM!")
        chan = await self.bot.create_channel(ctx.message.server, "game-planning")
        await self.bot.say("Game announced! To join, type `+` in {}!".format("<#" + chan.id + ">"))
        a = await self.bot.send_message(chan, "**PLANNING CHANNEL - Game run by {}!**\nType `+` to join.\nMax players: {}\n{}".format(ctx.message.author.mention, max_players, desc))
        b = await self.bot.send_message(chan, "Player List: None")
        await self.bot.pin_message(a)
        await self.bot.pin_message(b)
        game = {"dm": ctx.message.author, "players": set(), "planchan": chan, "maxp": max_players, "plistmsg": b}
        self.games.append(game)
        await self.bot.send_message(ctx.message.author, "Game started! Type `--` in the planning channel to end planning.")
        
def setup(bot):
    bot.add_cog(Scheduler(bot))