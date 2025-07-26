from icmplib import ping

import structlog

logger = structlog.get_logger()

class PingService:
    @staticmethod
    def ping_host(host: str, logger, count: int = 4, timeout: float = 2.0) -> dict:
        """
        Pings a host and returns the results.

        :param host: The hostname or IP address to ping.
        :param count: Number of echo requests to send.
        :param timeout: Timeout for each request in seconds.
        :return: A dictionary with the results of the ping.
        """
        logger.info("PING?", host=host, count=count, timeout=timeout)
        try:
            response = ping(host, count=count, timeout=timeout, privileged=False)
            logger.info("PONG", host=host, response=response)
            return {
                "host": host,
                "success": True,
                "min_rtt": response.min_rtt,
                "avg_rtt": response.avg_rtt,
                "max_rtt": response.max_rtt,
                "packet_loss": response.packet_loss
            }
        except Exception as e:
            return {
                "host": host,
                "success": False,
                "error": str(e)
            }