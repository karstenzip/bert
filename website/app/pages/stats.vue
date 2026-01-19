<template>
	<div
		v-auto-animate="{ duration: 400 }"
		class="flex flex-row flex-wrap gap-4 p-2"
	>
		<div
			v-for="stat in stats.slice().sort((a, b) => {
				if (b.value !== a.value) return b.value - a.value
				const keys = Object.keys(statNameMap)
				return keys.indexOf(a.name) - keys.indexOf(b.name)
			})"
			:key="stat.name"
			class="relative size-48 rounded-xl border border-gray-200"
			:class="{
				'animate-pulse': !streamReady
			}"
		>
			<h1 class="absolute top-4 right-4 left-4 font-bold">
				{{ statNameMap[stat.name] ?? stat.name }}
			</h1>
			<div class="flex h-full items-center justify-center p-0">
				<p class="text-5xl font-bold">
					{{
						stat.displayValue < 0
							? "Heh"
							: stat.displayValue < 1_000_000
								? stat.displayValue.toLocaleString()
								: "Tering"
					}}
				</p>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const guild = useGuild()

let stream: EventSource

const statNameMap = {
	messages_sent: "Berichten verzonden",
	characters_sent: "Tekens verzonden",
	numbers_used: "Aantal nummers gebruikt",
	words_sent: "Woorden verzonden",
	capital_letters_sent: "Hoofdletters verzonden",
	emojis_used: "Emoji's gebruikt",
	links_sent: "Links verzonden",
	images_sent: "Afbeeldingen verzonden",
	files_sent: "Bestanden verzonden",
	reactions_given: "Gegeven reacties",
	reactions_received: "Ontvangen reacties",
	times_mentioned: "Aantal keren genoemd",
	users_mentioned: "Aantal gebruikers genoemd"
}

type Stat = {
	name: keyof typeof statNameMap
	value: number
	displayValue: number
}

const stats = ref<Stat[]>([])
const streamReady = ref(false)

function animateValue(stat: Stat, newValue: number) {
	const start = stat.displayValue ?? 0
	const change = newValue - start
	const duration = 500
	const startTime = performance.now()

	function animate(now: number) {
		const elapsed = now - startTime
		const progress = Math.min(elapsed / duration, 1)
		stat.displayValue = Math.round(start + change * progress)
		if (progress < 1) {
			requestAnimationFrame(animate)
		} else {
			stat.displayValue = newValue
		}
	}
	requestAnimationFrame(animate)
}

onMounted(() => {
	watchEffect(async () => {
		if (stream) {
			console.log("Closing stats stream")
			stream.close()
			streamReady.value = false
		}
		stream = new EventSource(`/api/${guild.value}/stats`)
		stream.onopen = () => {
			console.log("Connected to stats stream")
		}
		stream.onmessage = (event) => {
			const data: Omit<Stat, "displayValue">[] = JSON.parse(event.data)
			if (!streamReady.value) {
				Object.keys(statNameMap).forEach((name) => {
					if (!data.some((item) => item.name === name)) {
						data.push({
							name: name as keyof typeof statNameMap,
							value: 0
						})
					}
				})
			}
			streamReady.value = true
			data.forEach((item) => {
				const existing = stats.value.find((stat) => stat.name === item.name)
				if (existing) {
					if (existing.value !== item.value) {
						animateValue(existing, item.value)
						existing.value = item.value
					}
				} else {
					const stat: Stat = {
						...item,
						displayValue: item.value
					}
					stats.value.push(stat)
				}
			})
		}
	})
})

onUnmounted(() => {
	if (stream) {
		console.log("Closing stats stream")
		stream.close()
	}
})
</script>
