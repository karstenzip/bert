import os
from supabase import AsyncClient, create_async_client

client: AsyncClient = None


async def init_supabase():
	global client
	client = await create_async_client(
		os.getenv("SUPABASE_URL"),
		os.getenv("SUPABASE_SECRET_KEY"),
	)
