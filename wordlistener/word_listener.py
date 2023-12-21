from redbot.core import Config, commands
import discord

class WordListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)
        self.config.register_guild(words=[])

    async def check_word(self, message):
        guild_words = await self.config.guild(message.guild).words()
        if not guild_words:
            return False

        for word in guild_words:
            if word.lower() in message.content.lower():
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if await self.check_word(message):
            guild_words = await self.config.guild(message.guild).words()
            if not guild_words:
                return
            
            matched_word = None
            for word in guild_words:
                if word.lower() in message.content.lower():
                    matched_word = word
                    break
            
            if matched_word:
                responses = {
                    'baciccio': discord.Embed(title="Parola Monitorata Trovata", description=f"Trovata parola: {matched_word}. Ora scrivo del testo"),
                    'ciccio': discord.Embed(title="Risposta per Parola 2", description="Descrizione per la Parola 2"),
                    # Aggiungi altre risposte per parole aggiuntive
                }
                
                if matched_word in responses:
                    embed = responses[matched_word]
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
    async def add_word(self, ctx, word: str):
        """Aggiunge una parola/frase da monitorare."""
        word = word.lower()
        async with self.config.guild(ctx.guild).words() as guild_words:
            if word not in guild_words:
                guild_words.append(word)
                await ctx.send(f"La parola '{word}' è stata aggiunta alla lista di parole monitorate.")
            else:
                await ctx.send(f"La parola '{word}' è già presente nella lista.")

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def remove_word(self, ctx, word: str):
        """Rimuove una parola/frase dalla lista monitorata."""
        word = word.lower()
        async with self.config.guild(ctx.guild).words() as guild_words:
            if word in guild_words:
                guild_words.remove(word)
                await ctx.send(f"La parola '{word}' è stata rimossa dalla lista di parole monitorate.")
            else:
                await ctx.send(f"La parola '{word}' non è presente nella lista.")

    @commands.command()
    @commands.guild_only()
    @commands.admin()
    async def list_words(self, ctx):
        """Mostra la lista delle parole/frasi monitorate."""
        guild_words = await self.config.guild(ctx.guild).words()
        if guild_words:
            word_list = "\n".join(guild_words)
            await ctx.send(f"Parole/frasi monitorate:\n{word_list}")
        else:
            await ctx.send("Nessuna parola/frase è attualmente monitorata.")

def setup(bot):
    bot.add_cog(WordListener(bot))
