import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

OWNER_ROLE = "OWNER"
CO_OWNER_ROLE = "Co-Owner"
HIGH_COMMAND_ROLE = "High Command"
CONTENT_MANAGER_ROLE = "Content Manager"
STAFF_ROLE = "STAFF"

def has_perms(interaction: discord.Interaction, role_name: str):
    # صاحب السيرفر دايما معاه صلاحية
    if interaction.user.id == interaction.guild.owner_id:
        return True
    # OWNER role
    if discord.utils.get(interaction.user.roles, name=OWNER_ROLE):
        return True
    if discord.utils.get(interaction.user.roles, name=role_name):
        return True
    return False

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands - Logged in as {bot.user}")
    except Exception as e:
        print(e)

# --- LOCK / UNLOCK SLASH ---
@bot.tree.command(name="lock", description="اقفل الكتابة عن رتبة معينة")
@app_commands.describe(role="اختار الرتبة اللي هتقفل عنها", channel="القناة (اختياري)")
async def lock_slash(interaction: discord.Interaction, role: discord.Role, channel: discord.TextChannel = None):
    if not has_perms(interaction, CO_OWNER_ROLE):
        return await interaction.response.send_message("❌ لازم رتبة Co-Owner او OWNER", ephemeral=True)
    channel = channel or interaction.channel
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = False
    overwrite.send_messages_in_threads = False
    overwrite.create_public_threads = False
    overwrite.embed_links = False
    overwrite.attach_files = False
    overwrite.add_reactions = False
    await channel.set_permissions(role, overwrite=overwrite)
    await interaction.response.send_message(f"🔒 قفلت {role.mention} في {channel.mention}")

@bot.tree.command(name="unlock", description="افتح الكتابة عن رتبة معينة")
@app_commands.describe(role="اختار الرتبة", channel="القناة (اختياري)")
async def unlock_slash(interaction: discord.Interaction, role: discord.Role, channel: discord.TextChannel = None):
    if not has_perms(interaction, CO_OWNER_ROLE):
        return await interaction.response.send_message("❌ لازم رتبة Co-Owner او OWNER", ephemeral=True)
    channel = channel or interaction.channel
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = True
    overwrite.send_messages_in_threads = True
    overwrite.create_public_threads = True
    overwrite.embed_links = True
    overwrite.attach_files = True
    overwrite.add_reactions = True
    await channel.set_permissions(role, overwrite=overwrite)
    await interaction.response.send_message(f"🔓 فتحت {role.mention} في {channel.mention}")

co_owner_cmds = ["ban","unban","kick","timeout","untimeout","slowmode","clear100","warn","addrole","removerole","nick","clear10","clear50","kickvc","move","mute","unmute","deafen","undeafen","lockchat","unlockchat"]
high_cmds = ["nems","video","pic","reel","short","post","editnews","deletenews","publish","unpublish","setthumb"]
staff_cmds = ["welcome","rules","helpme","ticket","support","info","faq","links","invite","server","membercount","ping"]
owner_only_cmds = ["eval","exec","shutdown","restart","reload","setowner","setcoowner","sethc","setcontent","setstaff"]

def make_slash(name, role_needed):
    async def callback(interaction: discord.Interaction):
        if not has_perms(interaction, role_needed):
            return await interaction.response.send_message(f"❌ محتاج رتبة {role_needed}", ephemeral=True)
        await interaction.response.send_message(f"✅ Executed: /{name}")
    return app_commands.Command(name=name, description=f"امر {name}", callback=callback)

for cmd in co_owner_cmds:
    bot.tree.add_command(make_slash(cmd, CO_OWNER_ROLE))
for cmd in high_cmds:
    bot.tree.add_command(make_slash(cmd, HIGH_COMMAND_ROLE))
for cmd in staff_cmds:
    bot.tree.add_command(make_slash(cmd, STAFF_ROLE))
for cmd in owner_only_cmds:
    bot.tree.add_command(make_slash(cmd, OWNER_ROLE))

@bot.tree.command(name="help", description="شوف كل اوامر البوت")
async def help_slash(interaction: discord.Interaction):
    embed = discord.Embed(title="📜 NOVA - كل الأوامر /", color=0x2b2d31)
    embed.add_field(name="🔒 قفل / فتح", value="`/lock @Role`\n`/unlock @Role`", inline=False)
    embed.add_field(name="👑 Co-Owner", value="`" + "`, `".join(co_owner_cmds) + "`", inline=False)
    embed.add_field(name="⚡ High Command", value="`" + "`, `".join(high_cmds) + "`", inline=False)
    embed.add_field(name="🛠️ STAFF", value="`" + "`, `".join(staff_cmds) + "`", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(os.getenv("TOKEN"))
