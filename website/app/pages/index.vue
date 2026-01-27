<template>
	<div class="flex h-full flex-col items-center pt-10">
		<h1 class="text-3xl font-bold">Bert</h1>
		<div class="absolute top-4 right-4">
			<button v-if="!user" @click="login">
				<Icon name="fluent:person-24-regular" size="48" aria-label="Log in" />
			</button>
			<NuxtLink v-else to="/dashboard">
				<img
					:src="user?.user_metadata?.avatar_url"
					class="size-12 rounded-full"
					alt="Avatar"
					aria-label="User avatar"
				/>
			</NuxtLink>
		</div>
	</div>
</template>

<script setup lang="ts">
definePageMeta({
	layout: "unauth"
})

const supabase = useSupabaseClient()
const user = useSupabaseUser()

async function login() {
	const { error } = await supabase.auth.signInWithOAuth({
		provider: "discord",
		options: {
			redirectTo: `${window.location.origin}/auth`
		}
	})
	if (error) console.log(error)
}
</script>
