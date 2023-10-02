import discord
import json
from discord.ext import commands

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filename = 'birthdays.json'  # JSON file to store all birthdays

    @commands.slash_command(name='add_birthday')
    async def add_birthday(self, ctx, user: discord.User, month: int, day: int, year: int):
        user_id = str(user.id)

        try:
            with open(self.filename, 'r') as f:
                all_birthdays = json.load(f)
        except FileNotFoundError:
            all_birthdays = {}

        all_birthdays[user_id] = {
            'day': day,
            'month': month,
            'year': year
        }

        with open(self.filename, 'w') as f:
            json.dump(all_birthdays, f)

        await ctx.respond(f'Birthday added for {user.display_name}: {day}/{month}/{year}')

    @commands.slash_command(name='get_birthday')
    async def get_birthday(self, ctx, user: discord.User = None):
        user_id = str(user.id) if user else str(ctx.author.id)

        try:
            with open(self.filename, 'r') as f:
                all_birthdays = json.load(f)
        except FileNotFoundError:
            await ctx.respond('No birthdays found.')
            return

        if user_id in all_birthdays:
            user_data = all_birthdays[user_id]
            day = user_data.get('day', 'N/A')
            month = user_data.get('month', 'N/A')
            year = user_data.get('year', 'N/A')
            await ctx.respond(f"{user.display_name}'s Birthday: {month}/{day}/{year}")
        else:
            await ctx.respond(f"No Birthday found for {user.display_name if user else ctx.author.display_name}")

    @commands.slash_command(name='delete_birthday')
    async def delete_birthday(self, ctx):
        user_id = str(ctx.author.id)

        try:
            with open(self.filename, 'r') as f:
                all_birthdays = json.load(f)
        except FileNotFoundError:
            await ctx.respond('No birthdays found.')
            return

        if user_id in all_birthdays:
            deleted_birthday = all_birthdays.pop(user_id)
            with open(self.filename, 'w') as f:
                json.dump(all_birthdays, f)
            response = f"Deleted birthday for {ctx.author.display_name}: {deleted_birthday['month']}/{deleted_birthday['day']}/{deleted_birthday['year']}"
        else:
            response = f"No birthday found for {ctx.author.display_name}"

        await ctx.respond(response)

    @commands.slash_command(name='upcoming_birthdays')
    async def upcoming_birthdays(self, ctx):
        server_id = str(ctx.guild.id) if ctx.guild else 'global'  # Use 'global' if the command is not in a server
        filename = f'upcoming_birthdays_{server_id}.json'  # Separate JSON file for upcoming birthdays

        try:
            with open(filename, 'r') as f:
                upcoming_birthdays = json.load(f)
        except FileNotFoundError:
            upcoming_birthdays = {}

        upcoming_bdays = []
        today = discord.utils.utcnow().date()

        for user_id, user_data in upcoming_birthdays.items():
            bday_date = discord.utils.parse_time(f"{user_data['year']}-{user_data['month']}-{user_data['day']}")
            if bday_date:
                bday_date = bday_date.date()
                if bday_date >= today:
                    user = self.bot.get_user(int(user_id))
                    if user:
                        upcoming_bdays.append((user.display_name, bday_date.strftime('%b %d')))

        if upcoming_bdays:
            upcoming_bdays.sort(key=lambda x: x[1])
            upcoming_bday_messages = [f"{user}: {date}" for user, date in upcoming_bdays]
            response = "Upcoming Birthdays:\n" + "\n".join(upcoming_bday_messages)
        else:
            response = 'No upcoming birthdays found in this server.'

        await ctx.respond(response)

def setup(bot):
    bot.add_cog(Birthday(bot))