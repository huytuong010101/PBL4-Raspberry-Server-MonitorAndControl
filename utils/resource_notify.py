import asyncio
import datetime
from typing import Callable
import psutil
from models.HardwareTracking import HardwareTracking
from threading import Thread
import asyncio


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


async def loop_to_notify_resource(send_message: Callable = None, delay: float = 1, delay_save=30):
    pre_time = datetime.datetime.now().timestamp()
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
        byte_send = net.bytes_sent
        byte_receive = net.bytes_recv
        network = {
            "send": get_size(byte_send),
            "receive": get_size(byte_receive),
            "byte_send": byte_send,
            "byte_receive": byte_receive
        }
        # get temperatures
        temperature = None
        if hasattr(psutil, "sensors_temperatures"):
            temperature = psutil.sensors_temperatures()["cpu_thermal"][0].current
        data = {
            "event": "update_resource",
            "data": {
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
                "network": network,
                "temperature": temperature,
            }
        }
        if send_message is not None:
            asyncio.get_event_loop().create_task(send_message(data, group="resource"))
        now = datetime.datetime.now()
        if now.timestamp() - pre_time > delay_save:
            pre_time = now.timestamp()
            save_data = {
                "time": now,
                "ram_percent": round(virtual.percent, 2),
                "cpu_percent": cpu["Total"],
                "temperature_percent": temperature,
                "network_send": byte_send,
                "network_receive": byte_receive,
            }
            Thread(target=lambda x: HardwareTracking.create_limit(x), args=(save_data,), daemon=True).start()
        await asyncio.sleep(delay)
