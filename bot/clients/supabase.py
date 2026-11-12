import os

from supabase import AsyncClient, create_async_client

client: AsyncClient = None  # ty: ignore[invalid-assignment]


async def init_supabase():
    global client
    client = await create_async_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SECRET_KEY"],
    )
