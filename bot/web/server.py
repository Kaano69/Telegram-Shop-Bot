from aiohttp import web
import logging

logger = logging.getLogger(__name__)

async def start_server():
    app = web.Application()
    
    # Define your routes here
    # Example: app.router.add_get('/', handle)

    return app

async def run_server():
    app = await start_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=8080)
    await site.start()
    logger.info("Server started at http://0.0.0.0:8080")

    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Shutdown initiated.")
    finally:
        await runner.cleanup()
        logger.info("Server shut down.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_server())