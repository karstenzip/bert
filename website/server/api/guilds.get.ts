export default defineEventHandler(async (event) => {
	const discordId: string = event.context.user.user_metadata.provider_id
	const guilds = await getGuildsWithMembers()

	return guilds
		.filter((guild) =>
			guild.members.some((member) => member.user.id === discordId)
		)
		.map((guild) => ({
			id: guild.id,
			name: guild.name,
			image: guild.icon
		}))
})
