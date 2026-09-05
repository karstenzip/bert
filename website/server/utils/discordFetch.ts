const { botToken } = useRuntimeConfig().discord

export default async function discordFetch<T>(endpoint: string): Promise<T> {
	const res = await $fetch<T>(endpoint, {
		baseURL: "https://discord.com/api/v10",
		headers: {
			Authorization: `Bot ${botToken}`
		}
	})
	return res as T
}
