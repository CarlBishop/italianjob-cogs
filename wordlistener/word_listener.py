from redbot.core import Config, commands
import discord

class WordListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='word_listener_config')

    async def check_word(self, message):
        words = await self.config.words()
        if words is None:
            return False

        print(f"Words in list: {words}")  # Stampiamo la lista delle parole per debug

        for word in words:
            if word.lower() in message.content.lower():
                print(f"Match found for word: {word}")  # Stampiamo il match per debug
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if await self.check_word(message):
            embed = discord.Embed(title="Parola Monitorata Trovata", description=message.content)
            embed.set_footer(text=f"Autore: {message.author.display_name}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)

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
