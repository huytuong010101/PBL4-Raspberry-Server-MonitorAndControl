import asyncio
import random
import psutil


async def loop_to_notify_resource(send_message=None, tracking=None):
    while True:
        data = {
            "cpu": round(psutil.cpu_percent(), 2),
            "ram": round(psutil.virtual_memory().percent, 2),
            "disk": round(psutil.disk_usage(psutil.disk_partitions()[0].mountpoint).percent, 2),
            "network": int(psutil.net_io_counters().bytes_sent/1000)
        }
        if send_message is not None:
            await send_message(data)
        if tracking is not None:
            tracking(data)
        await asyncio.sleep(1)
