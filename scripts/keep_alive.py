"""
keep_alive.py — Script to prevent the service container from exiting
when run in a minimal Docker environment without a process supervisor.
Useful for debugging or when running alongside other services.
"""
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("keep_alive: process started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("keep_alive: shutting down.")
