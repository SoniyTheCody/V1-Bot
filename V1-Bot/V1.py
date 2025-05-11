import discord
from discord.ext import commands
import datetime
import asyncio
import random
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

banned_words = ["bitch", "asshole", "dick"]
exceptions = ["fuck", "shit", "nigga"]

@bot.event
async def on_ready():
    print(f"[{bot.user}] SYSTEM ONLINE.")
    await bot.change_presence(activity=discord.Game(name="ULTRAKILL Mode"))

@bot.command(name="countdown")
async def countdown(ctx, days: int = 0, hours: int = 0, months: int = 0, *, msg="THE TIME HAS COME."):
    total_seconds = days * 86400 + hours * 3600 + months * 2592000
    await ctx.send(f"INITIATING COUNTDOWN: {months} months, {days} days, {hours} hours.")
    await asyncio.sleep(total_seconds)
    await ctx.send(f"@everyone {msg}")

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="TARGET INFORMATION", color=discord.Color.red())
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"VISUAL IDENTIFIER: {member.avatar.url}")

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="V1 COMMAND INTERFACE", color=discord.Color.blue())
    embed.add_field(name="!countdown <months> <days> <hours> <msg>", value="Activate countdown protocol.", inline=False)
    embed.add_field(name="!userinfo [user]", value="Retrieve user data.", inline=False)
    embed.add_field(name="!avatar [user]", value="Extract avatar.", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    lower_msg = message.content.lower()

    if "v1" in lower_msg:
        responses = [
            "V1... EXECUTION UNIT ACTIVE.",
            "YOU DARE SPEAK MY NAME?",
            "TARGET IDENTIFIED: ME.",
            "ULTRAKILL PROTOCOL READY.",
        ]
        await message.channel.send(random.choice(responses))

    for word in banned_words:
        if word in lower_msg and word not in exceptions:
            try:
                await message.author.send("UNACCEPTABLE LANGUAGE DETECTED. CEASE IMMEDIATELY.")
            except:
                pass
            for role in message.guild.roles:
                if "admin" in role.name.lower():
                    await message.channel.send(f"ADMIN ALERT: {message.author.mention} used inappropriate language.")
            break

    await bot.process_commands(message)

keep_alive()
bot.run(os.getenv("TOKEN"))
