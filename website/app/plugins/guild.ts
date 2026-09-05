export default defineNuxtPlugin(() => {
	const guild = useGuild()
	watch(guild, (guild) => {
		localStorage.setItem("guild", guild)
	})
})
