export default defineNuxtRouteMiddleware(async (to) => {
	if (to.meta.layout === "unauth") return
	const guild = useGuild()
	const isBertInstalled = useBertInstalled()

	if (!guild.value) {
		const storedGuild = localStorage.getItem("guild")
		if (storedGuild && /^\d{17,20}$/.test(storedGuild)) {
			isBertInstalled.value = true
			guild.value = storedGuild
		} else {
			const guilds = await $fetch("/api/guilds")
			if (guilds.length === 0) {
				isBertInstalled.value = false
				return
			}
			isBertInstalled.value = true
			const firstGuild = guilds[0]?.id
			guild.value = firstGuild ?? ""
		}
	}
})
