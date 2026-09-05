from asyncache import cached
from cachetools import TTLCache

from generic import bert


@cached(TTLCache(maxsize=1024, ttl=60 * 60))
async def get_team_members():
	app_info = await bert.application_info()
	return app_info.team.members
