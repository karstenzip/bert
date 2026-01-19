from generic import bert
from cachetools import TTLCache
from asyncache import cached


@cached(TTLCache(maxsize=1024, ttl=60 * 60))
async def get_team_members():
	app_info = await bert.application_info()
	return app_info.team.members
