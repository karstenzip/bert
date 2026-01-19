import type { APIApplication } from "discord-api-types/v10"

export default defineCachedFunction(
	async () => {
		const application = await discordFetch<APIApplication>("/applications/@me")
		return application.team!.members
	},
	{
		name: "discordTeamMembers",
		maxAge: 60 * 60 // 1 hour
	}
)
