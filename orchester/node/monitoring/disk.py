"""
Provides metrics collectors about disk usage

"""
import psutil


def get_global_disk_usage():
    """
    Return metrics about disk usage and disk IOs

    """
    disk_io = psutil.disk_io_counters()
    return [
        {'name': 'disk_usage',
         'value': psutil.disk_usage('.').percent,
         'unit': '%'},
        {'name': 'disk_io_reads',
         'value': disk_io.read_count},
        {'name': 'disk_io_writes',
         'value': disk_io.write_count},
        {'name': 'disk_io_read_bytes',
         'value': disk_io.read_bytes,
         'unit': 'bytes'},
        {'name': 'disk_io_write_bytes',
         'value': disk_io.write_bytes,
         'unit': 'bytes'},
        {'name': 'disk_io_read_time',
         'value': disk_io.read_time,
         'unit': 'us'},
        {'name': 'disk_io_write_time',
         'value': disk_io.write_time,
         'unit': 'us'},
        ]
