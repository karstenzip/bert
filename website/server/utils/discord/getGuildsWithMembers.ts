import type { APIGuildMember } from "discord-api-types/v10"

export default defineCachedFunction(
	async () => {
		const guilds = await getGuilds()
		return await Promise.all(
			guilds.map(async (guild) => {
				const members = await discordFetch<APIGuildMember[]>(
					`/guilds/${guild.id}/members?limit=1000`
				)
				return {
					...guild,
					members
				}
			})
		)
	},
	{
		name: "discordGuildMembers",
		maxAge: 60 * 60
	}
)
