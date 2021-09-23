import asyncio
import random
import psutil


async def loop_to_notify_resource(send_message=None, tracking=None):
    while True:
        data = {
            "cpu": int(psutil.cpu_percent()),
            "ram": int(psutil.virtual_memory().percent),
            "disk": int(psutil.disk_usage(psutil.disk_partitions()[0].mountpoint).percent),
            "network": int(psutil.net_io_counters().bytes_sent/1000)
        }
        if send_message is not None:
            await send_message(data)
        if tracking is not None:
            tracking(data)
        await asyncio.sleep(1)
