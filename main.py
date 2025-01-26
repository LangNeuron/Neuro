import asyncio


from settings.logger import get_logger
from neuro import neuro


async def main():
    neuro.run()


if __name__ == '__main__':
    logger = get_logger()
    asyncio.run(main())