<template>
	<aside
		class="sticky top-0 flex min-h-screen w-56 flex-col border-r border-gray-200 bg-[#fbfbfb] p-2 dark:bg-[#1e293b]"
	>
		<div class="flex flex-col items-center gap-y-2 p-2">
			<NuxtLink to="/dashboard" title="Bert">
				<Icon
					name="custom:bert"
					class="size-8"
					:class="{ 'animate-pulse': isLoading }"
				/>
			</NuxtLink>
			<USelectMenu
				v-model="localGuild"
				:avatar="localGuild?.avatar"
				:items="guilds"
				:search-input="false"
				class="w-full"
			/>
		</div>

		<div id="pages" class="menu">
			<NuxtLink to="/dashboard" title="Dashboard">
				<Icon name="fluent:home-48-filled" />
				Dashboard
			</NuxtLink>
			<NuxtLink to="/stats" title="Statistieken">
				<Icon name="fluent:number-symbol-16-filled" />
				Statistieken
			</NuxtLink>
		</div>

		<div id="control" class="menu mt-auto">
			<button title="Log uit" @click="logOut">
				<Icon name="fluent:arrow-exit-20-filled" />
				Log uit
			</button>
		</div>
	</aside>
</template>

<script setup lang="ts">
import type { SelectMenuItem } from "@nuxt/ui"

const supabase = useSupabaseClient()
const guild = useGuild()
const { isLoading } = useLoadingIndicator()

const guilds = (await $fetch("/api/guilds")).map(
	(guild) =>
		({
			label: guild.name,
			value: guild.id,
			avatar: {
				src: guild.image
					? `https://cdn.discordapp.com/icons/${guild.id}/${guild.image}.webp?size=20px`
					: undefined,
				alt: guild.name
			}
		}) satisfies SelectMenuItem
)
const localGuild = ref(guilds.find((g) => g.value === guild.value))

watch(localGuild, (newGuild) => {
	if (newGuild) {
		guild.value = newGuild.value
	}
})

async function logOut() {
	await supabase.auth.signOut()
	await navigateTo("/")
}
</script>

<style lang="scss">
.menu {
	display: flex;
	flex-direction: column;

	a,
	button {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.5rem 1rem;
		border-radius: 0.5rem;
		color: hsl(240 3.8% 45%);
		transition-property: color, background-color;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 150ms;

		@media (prefers-color-scheme: dark) {
			color: rgb(204, 208, 216);
		}

		&:hover {
			color: hsl(240 5.9% 10%);

			@media (prefers-color-scheme: dark) {
				color: #ffffff;
			}
		}

		&.router-link-active {
			color: hsl(240 5.9% 10%);
			border-radius: 0.5rem;
			background-color: #f4f4f5;

			@media (prefers-color-scheme: dark) {
				background-color: #afb5c0;
			}
		}
	}
}
</style>
