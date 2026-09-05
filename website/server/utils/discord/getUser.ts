import type { APIUser } from "discord-api-types/v10"

export default defineCachedFunction(
	async (id: string) => {
		return await discordFetch<APIUser>(`/users/${id}`)
	},
	{
		name: "discordUser",
		maxAge: 60 * 60 // 1 hour
	}
)
