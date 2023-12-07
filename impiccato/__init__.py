from .impiccato import Impiccato

__red_end_user_data_statement__ = 'This cog does not store user data.'

async def setup(bot):
    cog = Impiccato(bot)
    r = bot.add_cog(cog)
    if r is not None:
        await r
        await cog.initialize()
