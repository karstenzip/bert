export default async function verifyGuild(user_id: string, guild_id: string) {
	const guilds = await getGuildsWithMembers()
	return guilds.find(
		(guild) =>
			guild.id === guild_id &&
			guild.members.some((member) => member.user.id === user_id)
	)
}
