<template>
	<div class="flex size-full flex-col items-center justify-center">
		<div class="relative flex w-full flex-col items-center">
			<h1 class="absolute -top-20 text-5xl font-semibold">
				Hoi {{ user?.user_metadata?.full_name }} 👋
			</h1>

			<div v-if="suggestedAction === null" class="text-center">
				<p class="text-lg">Het is nu rustig, kijk gerust even rond</p>
			</div>
			<div
				v-else-if="suggestedAction.type === 'ADD_BOT'"
				class="flex flex-col items-center gap-4 rounded-lg border border-gray-300 bg-gray-100 p-4 text-lg dark:border-gray-800 dark:bg-gray-700"
			>
				<h2 class="text-2xl font-semibold">
					Je hebt Bert nog niet toegevoegd!
				</h2>

				<p>Voeg via onderstaande knop Bert toe aan je server</p>

				<NuxtLink
					:to="addBertUrl"
					rel="noopener noreferrer"
					target="_blank"
					class="flex items-center gap-x-2 rounded-full border border-gray-400/50 bg-gray-200 px-4 py-2 dark:bg-gray-900/75"
				>
					<Icon name="logos:discord-icon" />
					Voeg Bert toe
				</NuxtLink>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
const user = useSupabaseUser()

type SuggestedAction = {
	type: "ADD_BOT"
}

const isBertInstalled = useBertInstalled()

const suggestedAction = ref<SuggestedAction | null>(
	!isBertInstalled.value
		? {
				type: "ADD_BOT"
			}
		: null
)

const addBertUrl =
	"https://discord.com/oauth2/authorize?client_id=1173025279569035354"
</script>
