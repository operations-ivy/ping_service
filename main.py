import time

import structlog

from ping_service.ping import PingService
from ping_service.sql import SQLStorage

logger = structlog.get_logger(__name__)

if __name__ == "__main__":
    conn = SQLStorage.connect(":memory:")
    SQLStorage.create_table(conn)
    logger.info("Ping service started")
    while True:
        ping_service = PingService()
        result = ping_service.ping_host("8.8.8.8", logger)
        SQLStorage.insert_result(conn, result)
        logger.info("Sleeping for 10s")
        time.sleep(10)