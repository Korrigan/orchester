"""
This module provides all CPU related metrics collectors

"""

import psutil

def get_global_cpu_usage():
    """
    Return global metrics about CPU usage.

    """
    metrics = []
    metrics.append({
            'name': 'cpu_usage',
            'value': psutil.cpu_percent(interval=0),
            'unit': '%'
            })
    cpu_times = psutil.cpu_times_percent(interval=0)
    for t in ['system', 'user', 'idle',]:
        if hasattr(cpu_times, t):
            metrics.append({
                    'name': 'cpu_%s_time' % t,
                    'value': getattr(cpu_times, t),
                    'unit': '%'})
    return metrics
