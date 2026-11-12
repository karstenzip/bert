from cachetools import TTLCache
from discord import TeamMember

from async_cache import cached
from generic import bert


@cached(TTLCache(maxsize=1024, ttl=60 * 60))
async def get_team_members() -> list[TeamMember]:
	app_info = await bert.application_info()
	return app_info.team.members if app_info.team else []
