# ***************************************************************************#
#                                                                           #
# Background Axolotl                                                        #
# https://github.com/EndangeredNayla/Axolotl                                #
# Copyright (C) 2023 Nayla Hanegan. All rights reserved.                    #
#                                                                           #
# License:                                                                  #
# MIT License https://www.mit.edu/~amini/LICENSE.md                         #
#                                                                           #
# ***************************************************************************#
import discord
import os
import platform

from cogs.birthday import Birthday

from discord.ext import tasks
from discord.ext import commands

# Intents
intents = discord.Intents.all()

# Define Client
bot = commands.Bot(description="Birthday Bot", intents=intents)


@bot.event
async def on_ready():
    memberCount = len(set(bot.get_all_members()))
    serverCount = len(bot.guilds)
    print("Running as: " + bot.user.name + "#" + bot.user.discriminator)
    print(f"With Client ID: {bot.user.id}")
    print("\nBuilt With:")
    print("Python " + platform.python_version())
    print("Py-Cord " + discord.__version__)


# Boot Cogs
bot.add_cog(Birthday(bot))

# Run Bot
TOKEN = os.environ.get("BIRTHDAY_BOT")
bot.run(TOKEN)
