import discord
from discord import app_commands
from api import gui, commands

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Kb(bot=bot))

class Kb(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="keyboard", description="haha funny keyboard")
    async def keyboard(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=Keyboard(""))

class Keyboard(gui.PageUI):
    def __init__(self, data_transfer: str, page: int = 1):
        keys = sorted(list(set("ABCDEFGHIJKJMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-=_+[]{};':\"\\,.<>/?`~!@#$%^&*()")))
        super().__init__(element_count=len(keys), data_transfer=data_transfer, text=data_transfer, page=page)
        keys = keys[((self.page-1)*10):(self.page*10)]
        for key in keys:
            button = discord.ui.Button(label = key, style=discord.ButtonStyle.blurple, custom_id=key)
            button.callback = self.callback
            self.add_item(button)
        button = discord.ui.Button(label = "Backspace", style=discord.ButtonStyle.blurple, custom_id="backspace", row=4)
        button.callback = self.backspace
        self.add_item(button)
        button = discord.ui.Button(label = "Space", style=discord.ButtonStyle.blurple, custom_id="space", row=4)
        button.callback = self.space
        self.add_item(button)


    async def callback(self, interaction: discord.Interaction):
        self.data_transfer += interaction.data["custom_id"]
        await interaction.response.defer(ephemeral=True, thinking=False)
        await interaction.message.edit(content=self.data_transfer)

    async def backspace(self, interaction: discord.Interaction):
        self.data_transfer = self.data_transfer[:-1]
        await interaction.response.defer(ephemeral=True, thinking=False)
        await interaction.message.edit(content=self.data_transfer)

    async def space(self, interaction: discord.Interaction):
        self.data_transfer += " "
        await interaction.response.defer(ephemeral=True, thinking=False)
        await interaction.message.edit(content=self.data_transfer)

