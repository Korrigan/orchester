"""
This module provides helper functions to collect monitoring metrics for node
and workers.

It relies entirely on psutil library.

"""

import psutil

from . import cpu
from . import memory
from . import disk
from . import network

def get_global_metrics():
    """
    Retrieves global metrics from the system

    disk_usage path should be changed with the actual worker data
    mountpoint

    """
    metrics = []
    metrics.extend(cpu.get_global_cpu_usage())
    metrics.extend(memory.get_global_memory_usage())
    metrics.extend(disk.get_global_disk_usage())
    metrics.extend(network.get_global_network_usage())
    return metrics
