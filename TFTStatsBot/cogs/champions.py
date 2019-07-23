from discord.ext import commands
import requests
from discord import Embed
from disputils import BotEmbedPaginator


class Champions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BASEURL = "https://solomid-resources.s3.amazonaws.com/blitz/tft/data/champions.json"

    @commands.group(name="champ", aliases=["champion", "champs"], invoke_without_command=True)
    async def _champ(self, ctx):
        """Gets all available champions!

        Can only be executed on a server
        """
        row_data = requests.get(self.BASEURL)
        data = row_data.json()
        _champs = []
        for i in data:
            _champs.append(i)

        champs = ", ".join(_champs)
        embed = Embed(title="All available Champions:", description=f"```{champs}```")
        return await ctx.send(embed=embed)

    @_champ.command(name="info", aliases=["information"])
    @commands.cooldown(1, 6.0, commands.BucketType.user)
    async def _champ_info(self, ctx, *, name:str):
        """Gets information about a Champion!

        This command can only be executed on a server.
        """
        row_data = requests.get(url=self.BASEURL)
        data = row_data.json()
        _title = f"ChampInfo ~ {name}"
        __items = data[name]['items']

        embeds = [
            # General
            Embed(title=_title, description="__**General**__")
            .add_field(name="Origin:", value=data[name]["origin"][0], inline=False)
            .add_field(name="Class:", value=data[name]["class"][0], inline=False)
            .add_field(name="Cost:", value=data[name]["cost"], inline=False)
            .add_field(name="Items:", value=", ".join(__items), inline=False)
            .set_thumbnail(url=self.get_champ_img(name)),

            # Ability
            Embed(title=_title, description="__**Ability**__")
            .add_field(name="Name:", value=data[name]["ability"]["name"], inline=False)
            .add_field(name="Description:", value=data[name]["ability"]["description"], inline=False)
            .add_field(name="Type:", value=data[name]["ability"]["stats"][0]["type"], inline=False)
            .add_field(name="Value:", value=data[name]["ability"]["stats"][0]["value"], inline=False)
            .set_thumbnail(url=self.get_champ_img(name)),

            # Stats
            Embed(title=_title, description="__**Stats**__")
            .add_field(name="Offense", value=f"**Damage:** {data[name]['stats']['offense']['damage']}\n" 
                                             f"**Attack Speed:** {data[name]['stats']['offense']['attackSpeed']}\n" 
                                             f"**Damage per second:** {data[name]['stats']['offense']['dps']}\n" 
                                             f"**Range:** {data[name]['stats']['offense']['range']}", inline=False)
            .add_field(name="Defense", value=f"**Health:** {data[name]['stats']['defense']['health']}\n" 
                                             f"**Armor:** {data[name]['stats']['defense']['armor']}\n" 
                                             f"**Magic Resist:** {data[name]['stats']['defense']['magicResist']}", inline=False)
            .set_thumbnail(url=self.get_champ_img(name))
        ]

        paginator = BotEmbedPaginator(ctx, embeds)
        return await paginator.run()

    @staticmethod
    def get_champ_img(name:str):
        """Returns the image of an champion"""
        return f"https://ddragon.leagueoflegends.com/cdn/9.14.1/img/champion/{name}.png"


def setup(bot):
    bot.add_cog(Champions(bot))