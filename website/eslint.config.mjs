import eslintPluginPrettier from "eslint-plugin-prettier/recommended"
import { globalIgnores } from "eslint/config"
import withNuxt from "./.nuxt/eslint.config.mjs"

export default withNuxt(
	eslintPluginPrettier,
	globalIgnores(["shared/types/database.ts"]),
	{
		rules: {
			"vue/multi-word-component-names": "off",
			"@typescript-eslint/no-unused-vars": [
				"warn",
				{
					varsIgnorePattern: "^_",
					argsIgnorePattern: "^_"
				}
			]
		}
	}
)
