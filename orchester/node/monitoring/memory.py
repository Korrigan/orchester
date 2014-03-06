"""
Provide memory/swap related metrics collectors

"""
import psutil

def get_global_memory_usage():
    """
    Returns global ram/swap usage

    """
    return [
        {'name': 'ram_usage',
         'value': psutil.virtual_memory().percent,
         'unit': '%'},
        {'name': 'swap_usage',
         'value': psutil.swap_memory().percent,
         'unit': '%'}
        ]
