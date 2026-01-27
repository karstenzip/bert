<template>
	<div>
		<main>
			<slot />
		</main>
	</div>
</template>

<script setup lang="ts">
const user = useSupabaseUser()

watch(
	user,
	() => {
		if (user.value) {
			return navigateTo("/dashboard")
		}
	},
	{ immediate: true }
)
</script>
