<template>
	<div class="flex flex-row">
		<nav v-if="isBertInstalled">
			<Sidebar />
		</nav>
		<main class="p-2">
			<slot />
		</main>
	</div>
</template>

<script setup lang="ts">
const isBertInstalled = useBertInstalled()
</script>
