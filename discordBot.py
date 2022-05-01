import json

from discord.ext import commands
from MyBlackSwanCompare import MyBlackSwanCompare
from tools import Tools
import os

client = commands.Bot(command_prefix="/")


def validate_input_for_compare(i):
    if all([isinstance(word, str) for word in i.split(" ")]) or i.split(" ") != 2:
        return True
    return False


@client.command()
async def compare(ctx, *, i):
    if not validate_input_for_compare(i):
        await ctx.send("Input: {Crypto Symbol to compare to MyBlackSwan} {Dollars Per Day}")
    else:
        [os.remove(file) for file in os.listdir('./') if file.endswith('.png')]
        mbsc = MyBlackSwanCompare(i.split(" ")[0], int(i.split(" ")[1]),1)

        tools = Tools()
        tools.plotImage(mbsc.buildRevenueCompare(mbsc.buildPortfolioCompare()))
        tools.plotImage(mbsc.buildRevenueSwan())
        tools.saveImage(i.split(" ")[0] + '_vs_Swan.png')

        await ctx.send(str(json.loads(tools.uploadToImgur(i.split(" ")[0] + '_vs_Swan.png',i.split(" ")[0] + ' (blue) vs MyBlackSwan (orange)').text)['data']['link']))


@client.command()
async def compareraw(ctx, *, i):
    if not validate_input_for_compare(i):
        await ctx.send("Input: {Crypto Symbol to compare to MyBlackSwan} {Dollars Per Day}")
    else:
        mbsc = MyBlackSwanCompare(i.split(" ")[0], int(i.split(" ")[1]),1)
        comparePortfolio = (mbsc.buildPortfolioCompare())
        compareRevenue = str(mbsc.buildRevenueCompare(comparePortfolio))
        mbsRevenue = str(mbsc.buildRevenueSwan())
        mbscString = "MyBlackSwan Portfolio: " + str(mbsc.portfolio) + " Compare Portfolio: " + str(comparePortfolio) + " Compare Revenue: " + compareRevenue + " MyBlackSwan Revenue: " + mbsRevenue
        for chunk in [mbscString[i:i + 2000] for i in range(0, len(mbscString), 2000)]:
            await ctx.send(chunk)


@client.event
async def on_ready():
    print("Bot is ready")


client.run("")
