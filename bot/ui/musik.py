import typing

import discord
import wavelink


class MusicView(discord.ui.View):
    async def setup_player(self, interaction: discord.Interaction) -> wavelink.Player:
        assert interaction.guild is not None
        assert isinstance(interaction.user, discord.Member)
        player = typing.cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            user_channel = (
                interaction.user.voice.channel if interaction.user.voice else None
            )
            if not user_channel:
                await interaction.respond("You're not in a VC!", ephemeral=True)
                return player
            player = await user_channel.connect(cls=wavelink.Player)
            player.autoplay = wavelink.AutoPlayMode.partial
        return player


class AddBack(MusicView):
    def __init__(self, track: wavelink.Playable):
        super().__init__()
        self.track = track

    @discord.ui.button(label="Add back", style=discord.ButtonStyle.green, emoji="🔙")
    async def add_back(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        assert interaction.message is not None
        player = await self.setup_player(interaction)
        await player.queue.put_wait(self.track)
        if not player.playing:
            await player.play(player.queue.get(), volume=30)
        await interaction.response.send_message("Added back")
        button.disabled = True
        await interaction.followup.edit_message(
            message_id=interaction.message.id, view=self
        )


class RestoreQueue(MusicView):
    def __init__(self, queue: wavelink.Queue):
        super().__init__()
        self.queue = queue

    @discord.ui.button(label="Restore", style=discord.ButtonStyle.green, emoji="♻️")
    async def restore(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        assert interaction.message is not None
        player = await self.setup_player(interaction)
        for track in self.queue:
            await player.queue.put_wait(track)
        if not player.playing:
            await player.play(player.queue.get(), volume=30)
        await interaction.response.send_message("Queue restored")
        button.disabled = True
        await interaction.followup.edit_message(interaction.message.id, view=self)


class StopPlayer(MusicView):
    def __init__(self, ephemeral: bool):
        super().__init__()
        self.ephemeral = ephemeral

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red, emoji="⏹️")
    async def stop_player(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        assert interaction.message is not None
        assert interaction.guild is not None
        player = typing.cast(wavelink.Player, interaction.guild.voice_client)
        if not player:
            await interaction.response.send_message(
                "I'm not connected to a voice channel", ephemeral=self.ephemeral
            )
            return
        await player.disconnect()
        await interaction.response.send_message("Stopped", ephemeral=self.ephemeral)
        button.disabled = True
        await interaction.followup.edit_message(interaction.message.id, view=self)
