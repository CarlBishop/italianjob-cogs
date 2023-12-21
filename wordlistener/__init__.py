from .word_listener import WordListener

__red_end_user_data_statement__ = 'This cog does not store user data.'

async def setup(bot):
	await bot.add_cog(WordListener(bot))
	bot.add_command(WordListener.wordlistener_help)
