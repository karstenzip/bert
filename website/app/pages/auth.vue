<template>
	<div class="flex size-full items-center justify-center p-6">
		<Icon
			name="custom:bert"
			class="size-full"
			:class="{
				'animate-pulse': !isError,
				'text-red-700': isError
			}"
		/>
	</div>
</template>

<script setup lang="ts">
definePageMeta({
	layout: "unauth"
})

const user = useSupabaseUser()

const route = useRoute()
const isError = Boolean(route.query.error)
const errorDescription =
	route.query.error_description || "An unknown error occurred."
if (isError) {
	console.error("Authentication error:", errorDescription)
}

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
