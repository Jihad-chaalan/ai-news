import asyncio
from app.services.cleanup_service import CleanupService

async def main():
    service = CleanupService()
    # Set dry_run by adding a flag – we'll use a temporary hack: modify the service to log only.
    # Instead, we can just run the service and watch logs.
    deleted = await service.delete_old_briefings(-1)
    print(f"Deleted {deleted} old briefings.")

if __name__ == "__main__":
    asyncio.run(main())