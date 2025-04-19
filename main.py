import discord
from discord.ext import commands
import instaloader
import os
from dotenv import load_dotenv

# Environment variables load karo
load_dotenv()

# Bot prefix aur token set karo
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot = commands.Bot(command_prefix="!")

# Bot ready hone ka event
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

# Instagram Reels download command
@bot.command(name="reel")
async def download_reel(ctx, url):
    try:
        # Instaloader instance banaye
        L = instaloader.Instaloader()

        # Shortcode extract karo from URL
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Downloads folder banaye agar nahi hai
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        # Reel download karo
        L.download_post(post, target="downloads")

        # Download folder se video file dhundo
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                file_path = f"downloads/{file}"
                # File size check karo (Discord limit: 8MB for free users)
                if os.path.getsize(file_path) > 8 * 1024 * 1024:
                    await ctx.send("File size is too large! Discord free limit is 8MB.")
                    os.remove(file_path)
                    return
                
                # File Discord pe send karo
                await ctx.send(file=discord.File(file_path))
                
                # File delete karo cleanup ke liye
                os.remove(file_path)
                break
        else:
            await ctx.send("No video found in the post!")
            
    except Exception as e:
        await ctx.send(f"Error downloading reel: {str(e)}")

# Bot ko run karo
bot.run(BOT_TOKEN)
