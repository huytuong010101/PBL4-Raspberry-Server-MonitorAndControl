import asyncio
from typing import Callable
import psutil


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


async def loop_to_notify_resource(send_message: Callable = None, tracking: Callable = None, delay: float = 1):
    while True:
        # get cpu
        cpu = {}
        for i, p in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cpu[f"Core {i + 1}"] = round(p, 2)
        cpu["Total"] = round(psutil.cpu_percent(), 2)
        # get memory
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memory = {
            "Virtual":  {
                "total": get_size(virtual.total),
                "percent": round(virtual.percent, 2)
            },
            "Swap": {
                "total": get_size(swap.total),
                "percent": round(swap.percent, 2)
            }
        }
        # get disk
        disk = {}
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk[partition.mountpoint] = {
                    "total": get_size(partition_usage.total),
                    "percent": round(partition_usage.percent, 2)
                }
            except Exception:
                pass
        # get network
        net = psutil.net_io_counters()
        network = {
            "sent": get_size(net.bytes_sent),
            "receive": get_size(net.bytes_recv),
        }
        # get temperatures
        temperature = None
        if hasattr(psutil, "sensors_temperatures"):
            temperature = psutil.sensors_temperatures()["cpu_thermal"][0].current
        data = {
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
            "network": network,
            "temperature": temperature,
        }
        if send_message is not None:
            await send_message(data)
        if tracking is not None:
            await tracking(data)
        await asyncio.sleep(delay)
