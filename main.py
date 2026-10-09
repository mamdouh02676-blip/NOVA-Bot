import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

OWNER_ROLE = "OWNER"
CO_OWNER_ROLE = "Co-Owner"
HIGH_COMMAND_ROLE = "High Command"
CONTENT_MANAGER_ROLE = "Content Manager"
STAFF_ROLE = "STAFF"

def has_role_or_owner(role_name):
    async def predicate(ctx):
        if discord.utils.get(ctx.author.roles, name=OWNER_ROLE):
            return True
        if discord.utils.get(ctx.author.roles, name=role_name):
            return True
        return False
    return commands.check(predicate)

@bot.command(name="lock")
@has_role_or_owner(CO_OWNER_ROLE)
async def lock_cmd(ctx, role: discord.Role, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = False
    overwrite.send_messages_in_threads = False
    overwrite.create_public_threads = False
    overwrite.embed_links = False
    overwrite.attach_files = False
    overwrite.add_reactions = False
    overwrite.use_external_emojis = False
    await channel.set_permissions(role, overwrite=overwrite)
    await ctx.send(f"Locked {role.name} in {channel.mention} as screenshot")

@bot.command(name="unlock")
@has_role_or_owner(CO_OWNER_ROLE)
async def unlock_cmd(ctx, role: discord.Role, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(role)
    overwrite.send_messages = True
    overwrite.send_messages_in_threads = True
    overwrite.create_public_threads = True
    overwrite.embed_links = True
    overwrite.attach_files = True
    overwrite.add_reactions = True
    overwrite.use_external_emojis = True
    await channel.set_permissions(role, overwrite=overwrite)
    await ctx.send(f"Unlocked {role.name} in {channel.mention}")

co_owner_cmds = ["ban","unban","kick","timeout","untimeout","slowmode","clear100","warn","addrole","removerole","nick","announce","g_announce","dm","botrestart","setprefix","antiraid_on","antiraid_off","whitelist","blacklist","serverinfo","userinfo","roleinfo","channelinfo","createchannel","deletechannel","createrole","deleterole","moveall","muteall","unmuteall","deafenall","undeafenall","giveaway","g_end","g_reroll","ticket_closeall","backup","setlogs","setwelcome","setrules","setautorole","audit","lockall","unlockall","purge","nuke","sayall"]
high_cmds = ["clear10","clear25","clear50","kickvc","move","mute","unmute","deafen","undeafen","lockchat","unlockchat","hide","unhide","slow5","slow10","slowoff","pin","unpin","poll","say","embed","ticket_add","ticket_remove","ticket_close","voicelock","voiceunlock","voicelimit","baninfo","invites","avatar","banner","role_members","purge_bot","purge_links","purge_images","purge_user","tempban","softban","temp_mute_1h","temp_mute_24h","reason","history","report","vcmove","warn1","warn2","warn3","invites_check","userinfo_hc"]
content_cmds = ["news","video","pic","reel","short","post","editnews","deletenews","publish","unpublish","setthumb","settitle","setdesc","settags","schedule_post","live","golive","stoplive","clip","highlight","trending","qotd","event_create","event_start","event_end","giveaway_content","poll_content","meme","funfact","update_log","patchnote","leak","spoiler","announce_content","youtube","tiktok","insta","twitch","embed_news","embed_video","content_stats","top_post","set_content_channel","set_news_channel","set_video_channel","content_help","content_rules","content_ban","content_unban"]
staff_cmds = ["welcome","rules","help","ticket","support","info","faq","links","invite","server","membercount","ping","uptime","afk","unafk","remind","calc","avatar_s","banner_s","userinfo_s","roleinfo_s","poll_s","say_s","embed_s","8ball","meme_s","joke","quote","fact","weather","translate","search","youtube_s","play","stop","skip","queue","pause","resume","volume","lyrics","report_s","suggest","feedback","close","open","slowmode_s","clear5","warn_s","ticket_s"]
owner_only_cmds = ["eval","exec","shutdown","restart","reload","setowner","setcoowner","sethc","setcontent","setstaff","owner1","owner2","owner3","owner4","owner5","owner6","owner7","owner8","owner9","owner10","owner11","owner12","owner13","owner14","owner15","owner16","owner17","owner18","owner19","owner20","owner21","owner22","owner23","owner24","owner25","owner26","owner27","owner28","owner29","owner30","owner31","owner32","owner33","owner34","owner35","owner36","owner37","owner38","owner39","owner40","owner41","owner42","owner43","owner44","owner45"]

for cmd in co_owner_cmds:
    @bot.command(name=cmd)
    @has_role_or_owner(CO_OWNER_ROLE)
    async def co_c(ctx, cmd=cmd): await ctx.send(f"Executed: {cmd}")
for cmd in high_cmds:
    @bot.command(name=cmd)
    @has_role_or_owner(HIGH_COMMAND_ROLE)
    async def hc_c(ctx, cmd=cmd): await ctx.send(f"Executed: {cmd}")
for cmd in content_cmds:
    @bot.command(name=cmd)
    @has_role_or_owner(CONTENT_MANAGER_ROLE)
    async def cm_c(ctx, cmd=cmd): await ctx.send(f"Executed: {cmd}")
for cmd in staff_cmds:
    @bot.command(name=cmd)
    @has_role_or_owner(STAFF_ROLE)
    async def staff_c(ctx, cmd=cmd): await ctx.send(f"Executed: {cmd}")
for cmd in owner_only_cmds:
    @bot.command(name=cmd)
    @has_role_or_owner(OWNER_ROLE)
    async def owner_c(ctx, cmd=cmd): await ctx.send(f"OWNER ONLY Executed: {cmd}")
