export function discordAvatarUrl(
	userId: string,
	avatarHash: string,
	options: { size: number } | undefined = { size: 128 }
) {
	const baseUrl = "https://cdn.discordapp.com/avatars"
	const query = new URLSearchParams({
		size: options.size.toString()
	})
	return `${baseUrl}/${userId}/${avatarHash}.webp?${query.toString()}`
}
