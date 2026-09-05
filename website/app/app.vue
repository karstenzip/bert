<template>
	<NuxtLayout id="root" class="h-screen">
		<UApp>
			<NuxtPage />
		</UApp>
	</NuxtLayout>
</template>

<script setup lang="ts">
useHead({
	title: "Bert",
	link: [
		{
			rel: "icon",
			type: "image/svg",
			href: "/bert.svg"
		}
	]
})
</script>

<style lang="scss">
#root {
	display: flex;
	flex-direction: row;

	main {
		flex: auto;
	}
}
</style>
