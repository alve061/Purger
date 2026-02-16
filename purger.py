import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, chunk_guilds_at_startup=False)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="purge", description="Delete up to 100 messages at a time")
@app_commands.describe(amount="Amount of messages to be deleted (1-100)")
async def purge(interaction: discord.Interaction, amount: int):
    # Fast upfront validation before any API calls
    if amount < 1 or amount > 100:
        await interaction.response.send_message(
            "Please provide a number between 1 and 100!",
            ephemeral=True
        )
        return

    # Permission checks use cached data - no extra API calls
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "You need the 'Manage Messages' permission to use this command!",
            ephemeral=True
        )
        return

    if not interaction.guild.me.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "I need the 'Manage Messages' permission to purge messages!",
            ephemeral=True
        )
        return

    # Defer immediately to beat Discord's 3s interaction timeout
    await interaction.response.defer(ephemeral=True)

    try:
        deleted = await interaction.channel.purge(
            limit=amount,
            oldest_first=False,
            bulk=True  # Bulk delete is significantly faster than one-by-one
        )

        if len(deleted) == 0:
            await interaction.followup.send(
                "Couldn't delete any messages due to Discord limitations. All of the affected messages were too old.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"Deleted {len(deleted)} message(s).",
                ephemeral=True
            )

        print(f"[{datetime.now()}] {interaction.user} purged {len(deleted)} messages in {interaction.guild.name} - #{interaction.channel.name}")

    except discord.Forbidden:
        await interaction.followup.send(
            "I don't have permission to delete messages in this channel!",
            ephemeral=True
        )
    except discord.HTTPException as e:
        await interaction.followup.send(
            f"An error occurred while deleting messages: {str(e)}",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"An unexpected error occurred: {str(e)}",
            ephemeral=True
        )

# Run the bot
if __name__ == "__main__":
    # Get token from environment variable
    TOKEN = ('')
    
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN environment variable not set!")
        print("  Windows: set DISCORD_BOT_TOKEN=your_token_here")
        exit(1)
    
    bot.run(TOKEN, log_handler=None)
