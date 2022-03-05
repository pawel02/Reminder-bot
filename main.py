from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/")

tasks = []

async def send_reminder(ctx, reminder, wait_time):
    # Get all the users by searching for the @
    members = ctx.message.mentions
    await asyncio.sleep(wait_time)
    
    for member in members:
        await member.send(reminder)
    await ctx.send(reminder)

@bot.command(name="reminder", aliases=['r'], help="""
    Create a reminder default time is 6 hours 
    and an optional date at the end for example with @users for the people you want to send dms to
    'This is a custom reminder @Computeshorts @Jinxed 02:05:20:30'
""")
async def create_reminder(ctx, *args):
    # Parse the date
    days      = 0
    hours     = 6
    minutes   = 0
    seconds   = 0

    # If the last argument is a date
    if ":" in args[-1]:
        hours = 0
        time = args[-1].split(":")

        # If its not in the correct format just ignore since it could be part of the message
        if len(time) == 4:
            days    = int(time[0])
            hours   = int(time[1])
            minutes = int(time[2])
            seconds = int(time[3])

    seconds = seconds + (minutes * 60) + (hours * 60 * 60) + (days * 24 * 60 * 60)
    task = asyncio.create_task(send_reminder(ctx, " ".join(args[:-1]), seconds))
    tasks.append(task)
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled")

@bot.command(name="clear", aliases=["c"], help="Clears all the reminders")
async def clear_reminders(ctx, *args):
    for t in tasks:
        t.cancel()

bot.run('OTQ5NjE1MDM0NzE4Mzg0MTY4.YiM76w.EaW8XMSzjVllKTlUrpZNTYcGBaQ')

