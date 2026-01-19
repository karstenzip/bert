from discord import ApplicationContext, VoiceChannel
from discord.ext.commands import check
from generic import bert
import wavelink

from utils.discord import get_team_members


def require_vc(cls=wavelink.Player):
	"""Join the voice channel before running the command. Use the `channel` option to specify a channel."""

	async def predicate(ctx: ApplicationContext):
		channel: VoiceChannel | None = next(
			(
				bert.get_channel(int(item["value"]))
				for item in ctx.interaction.data.get("options", [])
				if item["name"] == "channel"
			),
			None,
		)

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

		voice_channel: VoiceChannel | None = ctx.user.voice.channel
		if ctx.voice_client:
			if voice_channel != ctx.voice_client.channel:
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
			else:
				await voice_channel.connect(cls=cls)
				return True  # Connected to user's channel

	return check(predicate)


def admin_only():
	"""Only allows team members to use the command."""

	async def predicate(ctx: ApplicationContext):
		team_members = await get_team_members()
		if ctx.user not in team_members:
			await ctx.respond(
				"You are unauthorized to perform this action", ephemeral=True
			)
			return False
		return True

	return check(predicate)
