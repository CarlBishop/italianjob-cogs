from redbot.core import Config, commands
import discord

class WordListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)
        self.config.register_guild(monitored_words={})  # Cambio del nome del valore 'words'
        
    async def check_word(self, message):
        guild_words = await self.config.guild(message.guild).monitored_words()
        if not guild_words:
            return False

        for word, embed_data in guild_words.items():
            if word.lower() in message.content.lower():
                return word, embed_data
        return False

    @commands.command(name="wordlistener")
    async def wordlistener_help(self, ctx):
        """Comando di aiuto per il cog WordListener."""
        help_embed = discord.Embed(title="Aiuto per il WordListener",
                                   description="Ecco i comandi disponibili per il WordListener cog:")
        help_embed.add_field(name="add_word", value='Aggiunge una parola/frase da monitorare. Esempio  add_word parola {"title": "Titolo", "description": "Descrizione"}')
        help_embed.add_field(name="remove_word", value="Rimuove una parola/frase dalla lista monitorata.")
        help_embed.add_field(name="list_words", value="Mostra la lista delle parole/frasi monitorate.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        word_data = await self.check_word(message)
        if word_data:
            word, embed_data = word_data
            if embed_data:
                embed = discord.Embed.from_dict(embed_data)
                author = message.author
                if isinstance(author, discord.Member):
                    if author.avatar:
                        embed.set_footer(text=f"Autore: {author.display_name}", icon_url=author.avatar.url)
                    else:
                        embed.set_footer(text=f"Autore: {author.display_name}")
                else:
                    embed.set_footer(text=f"Autore: {author.display_name}")
                await message.channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def add_word(self, ctx, word: str, *, embed_data: str):
        """Aggiunge una parola/frase da monitorare con un embed associato."""
        word = word.lower()
        async with self.config.guild(ctx.guild).monitored_words() as guild_words:
            if word not in guild_words:
                embed_dict = eval(embed_data)  # Converti i dati dell'embed in un dizionario
                guild_words[word] = embed_dict
                await ctx.send(f"La parola '{word}' è stata aggiunta alla lista di parole monitorate con l'embed associato.")
            else:
                await ctx.send(f"La parola '{word}' è già presente nella lista.")

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def remove_word(self, ctx, word: str):
        """Rimuove una parola/frase dalla lista monitorata."""
        word = word.lower()
        async with self.config.guild(ctx.guild).monitored_words() as guild_words:
            if word in guild_words:
                del guild_words[word]
                await ctx.send(f"La parola '{word}' è stata rimossa dalla lista di parole monitorate.")
            else:
                await ctx.send(f"La parola '{word}' non è presente nella lista.")

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def list_words(self, ctx):
        """Mostra la lista delle parole/frasi monitorate."""
        guild_words = await self.config.guild(ctx.guild).monitored_words()
        if guild_words:
            word_list = "\n".join(guild_words.keys())
            await ctx.send(f"Parole/frasi monitorate:\n{word_list}")
        else:
            await ctx.send("Nessuna parola/frase è attualmente monitorata.")

def setup(bot):
    bot.add_cog(WordListener(bot))
