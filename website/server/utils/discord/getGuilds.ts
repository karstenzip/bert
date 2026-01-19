import type { APIGuild } from "discord-api-types/v10"

export default defineCachedFunction(
	async () => {
		return await discordFetch<APIGuild[]>("/users/@me/guilds")
	},
	{
		name: "discordGuilds",
		maxAge: 60
	}
)
