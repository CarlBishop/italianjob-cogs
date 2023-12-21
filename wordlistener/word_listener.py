from redbot.core import Config, commands

class WordListener(commands.Cog):
    """Cog per ascoltare determinate parole/frasi e rispondere con un embed."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='word_listener_config')

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def add_word(self, ctx, word: str):
        """Aggiunge una parola/frase da monitorare."""
        word = word.lower()
        words = await self.config.words()
        if words is None:
            words = []  # Inizializza words come una lista vuota se è None
        if word not in words:
            words.append(word)
            await self.config.words.set(words)
            await ctx.send(f"La parola '{word}' è stata aggiunta alla lista di parole monitorate.")
        else:
            await ctx.send(f"La parola '{word}' è già presente nella lista.")

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def remove_word(self, ctx, word: str):
        """Rimuove una parola/frase dalla lista monitorata."""
        word = word.lower()
        words = await self.config.words()
        if word in words:
            words.remove(word)
            await self.config.words.set(words)
            await ctx.send(f"La parola '{word}' è stata rimossa dalla lista di parole monitorate.")
        else:
            await ctx.send(f"La parola '{word}' non è presente nella lista.")

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def list_words(self, ctx):
        """Mostra la lista delle parole/frasi monitorate."""
        words = await self.config.words()
        if words:
            word_list = "\n".join(words)
            await ctx.send(f"Parole/frasi monitorate:\n{word_list}")
        else:
            await ctx.send("Nessuna parola/frase è attualmente monitorata.")

def setup(bot):
    bot.add_cog(WordListener(bot))
