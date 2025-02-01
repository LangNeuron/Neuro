import asyncio
import threading
import time


from settings.constant import data
from settings.logger import get_logger
from signals import Signals
from neuro import Neuro
from web import Web


async def main():
    signal = Signals()
    web = Web(data["Web"]["Name"], signal, data["Web"]["config_object"])
    neuro = Neuro(signal)
    neuro_run = threading.Thread(target=neuro.run)
    web_run = threading.Thread(target=web.run)
    try:
        neuro_run.start()
        web_run.start()
        while signal.terminate is False:
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(e)
    finally:
        signal.terminate = True
        time.sleep(5)
        web_run.join()
        neuro_run.join()
    logger.info("Program terminated")


if __name__ == "__main__":
    logger = get_logger()
    asyncio.run(main())
