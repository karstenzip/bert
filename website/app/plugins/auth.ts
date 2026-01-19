export default defineNuxtPlugin(() => {
	const admin = useIsAdmin()
	const user = useSupabaseUser()
	watch(user, async (user) => {
		if (!user) {
			admin.value = undefined
		}
	})
})
