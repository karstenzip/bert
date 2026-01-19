export const useBertInstalled = () => useState<boolean>(() => false)
export const useGuild = () => useState<string>(() => "")
export const useIsAdmin = () => useState<boolean | undefined>(() => undefined)
