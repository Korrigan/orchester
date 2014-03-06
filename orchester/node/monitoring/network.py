"""
Provides all network related metrics collectors

"""
import psutil

def get_global_network_usage():
    """
    Returns network metrics

    """
    net_io = psutil.net_io_counters()
    return [
        {'name': 'net_in_bytes',
         'value': net_io.bytes_recv,
         'unit': 'bytes'},
        {'name': 'net_out_bytes',
         'value': net_io.bytes_sent,
         'unit': 'bytes'},
        {'name': 'net_in_errors',
         'value': net_io.errin},
        {'name': 'net_out_errors',
         'value': net_io.errout
         },
        ]
