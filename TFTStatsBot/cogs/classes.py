from discord.ext import commands
from discord import Embed
import requests

class Classes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CHAMPURL = "https://solomid-resources.s3.amazonaws.com/blitz/tft/data/champions.json"

    @commands.group(name="class", invoke_without_command=True)
    @commands.cooldown(1, 6.0, commands.BucketType.user)
    async def _class(self, ctx, *, name:str):
        """Gets the champions who belongs to a class!

        This command can only be executed on a server.
        """
        _champs = []
        row_data = requests.get(self.CHAMPURL)
        data = row_data.json()

        for i in data:
            if data[i]["class"][0] == name.capitalize():
                _champs.append(i)

        champs = ", \n".join(_champs)
        embed = Embed(title=f"All {name.capitalize()} Champs", description=champs)
        return await ctx.send(embed=embed)

    @staticmethod
    def get_class_img(name):
        """Gets the image of a class"""
        pass

def setup(bot):
    bot.add_cog(Classes(bot))