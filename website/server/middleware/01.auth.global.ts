import { serverSupabaseUser } from "#supabase/server"

const adminOnlyPaths: RegExp[] = []

export default defineEventHandler(async (event) => {
	if (!event.path.startsWith("/api/")) return
	const user = await serverSupabaseUser(event)
	if (!user) {
		throw createError({ statusCode: 401, statusMessage: "Unauthorized" })
	}

	if (adminOnlyPaths.some((path) => event.path.match(path))) {
		const members = await getTeamMembers()
		const isMember = members.some(
			(member) => member.user.id === user.user_metadata?.provider_id
		)
		if (!isMember) {
			throw createError({ statusCode: 403, statusMessage: "Forbidden" })
		}
	}
	event.context.user = user
})
