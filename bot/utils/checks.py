import discord
import wavelink
from discord.ext.commands import Context, check

from generic import bert
from utils.discord import get_team_members


def require_vc(cls=wavelink.Player):
    """Join the voice channel before running the command. Use the `channel` option to specify a channel."""

    async def predicate(ctx: Context):
        assert isinstance(ctx, discord.ApplicationContext)
        assert isinstance(ctx.user, discord.Member)
        assert ctx.interaction.data is not None

        channel = next(
            (
                bert.get_channel(int(item.get("value", 0)))
                for item in ctx.interaction.data.get("options", [])
                if item["name"] == "channel"
            ),
            None,
        )

        if channel is not None and not isinstance(channel, discord.VoiceChannel):
            await ctx.respond("You can only select a voice channel", ephemeral=True)
            return False

        if not ctx.user.voice and not channel:
            await ctx.respond(
                "You must be in a voice channel to use this command.", ephemeral=True
            )
            return False  # No user's voice channel nor specified voice channel
        if channel and not [member for member in channel.members if not member.bot]:
            await ctx.respond(
                "That's an empty voice channel (or it only has bots)!", ephemeral=True
            )
            return False  # Don't join empty channels

        user_channel = ctx.user.voice.channel if ctx.user.voice else None
        if ctx.voice_client:
            if user_channel != ctx.voice_client.channel:
                await ctx.respond(
                    "I'm already playing in another channel!", ephemeral=True
                )
                return False  # Don't allow switching channels
            else:
                return True  # Already connected
        else:
            if channel:
                await channel.connect(cls=cls)
                return True  # Connected to specified channel
            elif user_channel:
                await user_channel.connect(cls=cls)
                return True  # Connected to user's channel
            else:
                return False  # Neither bot nor user are connected and a desired channel isn't given

    return check(predicate)


def admin_only():
    """Only allows team members to use the command."""

    async def predicate(ctx: Context):
        assert isinstance(ctx, discord.ApplicationContext)
        team_members = await get_team_members()
        if ctx.user not in team_members:
            await ctx.respond(
                "You are unauthorized to perform this action", ephemeral=True
            )
            return False
        return True

    return check(predicate)
