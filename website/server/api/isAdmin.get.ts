export default defineEventHandler(async (event) => {
	const { user } = event.context
	const members = await getTeamMembers()
	const isMember = members.some(
		(member) => member.user.id === user?.user_metadata.provider_id
	)
	return isMember
})
