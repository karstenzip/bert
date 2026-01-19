export default defineNuxtRouteMiddleware(async (to) => {
	const isAdmin = useIsAdmin()
	const user = useSupabaseUser()
	if (user.value && isAdmin.value === undefined) {
		const { data } = await useFetch("/api/isAdmin")
		isAdmin.value = data.value ?? false
	}
	if (to.meta.adminOnly) {
		if (!isAdmin.value)
			throw createError({
				statusCode: 404,
				statusMessage: `Page not found: ${to.fullPath}`
			})
	}
})
