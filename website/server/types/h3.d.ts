import type { Claims } from "@supabase/auth-js"

declare module "h3" {
	interface H3EventContext {
		user: Claims
	}
}
