export default defineNuxtConfig({
	modules: [
		"@nuxtjs/supabase",
		"@nuxt/ui",
		"@formkit/auto-animate/nuxt",
		"@nuxt/eslint"
	],
	runtimeConfig: {
		discord: {
			botToken: ""
		}
	},
	supabase: {
		redirectOptions: {
			login: "/",
			callback: "/auth"
		},
		types: "#shared/types/database.ts"
	},
	routeRules: {
		"/github": {
			redirect: "https://github.com/karstenzip/bert"
		}
	},
	typescript: {
		typeCheck: true
	},
	css: ["~/assets/css/darkmode.css", "~/assets/css/main.css"],
	icon: {
		mode: "svg",
		customCollections: [
			{
				prefix: "custom",
				dir: "./app/assets/icons"
			}
		],
		clientBundle: {
			scan: true,
			includeCustomCollections: true
		}
	},
	ssr: false,
	nitro: {
		preset: "bun",
		imports: {
			imports: [{ name: "*", as: "z", from: "zod/v4" }]
		}
	},
	compatibilityDate: "2025-07-15",
	devtools: {
		enabled: true
	},
	devServer: {
		port: 6969
	}
})
