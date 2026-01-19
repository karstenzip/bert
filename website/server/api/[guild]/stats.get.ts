import { serverSupabaseServiceRole } from "#supabase/server"

const schema = z.object({
	guild: z.string().regex(/^\d{17,20}$/)
})

export default defineEventHandler(async (event) => {
	const stream = createEventStream(event)
	const { guild } = await getValidatedRouterParams(event, schema.parse)
	const discordId: string = event.context.user.user_metadata.provider_id

	if (!(await verifyGuild(discordId, guild))) {
		throw createError({ statusCode: 404, statusMessage: "Guild not found" })
	}

	const client = serverSupabaseServiceRole(event)
	const channel = client.channel("stats").on<Tables<"stats">>(
		"postgres_changes",
		{
			event: "*",
			schema: "public",
			table: "stats",
			filter: `user_id=eq.${discordId}` // Only one filter is currently supported: https://github.com/supabase/realtime/issues/486
		},
		(payload) => {
			const data = payload.new as Tables<"stats">
			if (data.guild_id !== guild) return
			if (batch.find((item) => item.name === data.name)) {
				batch = batch.map((item) =>
					item.name === data.name ? { ...item, value: data.value } : item
				)
			} else {
				batch.push({ name: data.name, value: data.value })
			}
			if (!batchTimeout) {
				batchTimeout = setTimeout(async () => {
					await stream.push(`${JSON.stringify(batch)}\n\n`)
					batch = []
					batchTimeout = undefined
				})
			}
		}
	)

	let batch: { name: string; value: number }[] = []
	let batchTimeout: NodeJS.Timeout | undefined

	const { data } = await client
		.from("stats")
		.select("name,value")
		.eq("user_id", discordId)
		.eq("guild_id", guild)

	setTimeout(async () => {
		await stream.push(JSON.stringify(data ?? []) + "\n\n")
		channel.subscribe()
	})

	stream.onClosed(() => {
		client.removeChannel(channel)
		clearTimeout(batchTimeout)
	})

	return stream.send()
})
