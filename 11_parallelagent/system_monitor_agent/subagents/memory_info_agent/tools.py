import time
from typing import Any, Dict

import psutil


def get_memory_info() -> Dict[str, Any]:
    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        memory_info = {
            "total_memory": f"{memory.total / (1024 ** 3):.2f} GB",
            "available_memory": f"{memory.available / (1024 ** 3):.2f} GB",
            "used_memory": f"{memory.used / (1024 ** 3):.2f} GB",
            "memory_percentage": f"{memory.percent:.1f}%",
            "swap_total": f"{swap.total / (1024 ** 3):.2f} GB",
            "swap_used": f"{swap.used / (1024 ** 3):.2f} GB",
            "swap_percentage": f"{swap.percent:.1f}%",
        }

        return {
            "result": memory_info,
            "stats": {
                "memory_usage_percentage": memory.percent,
                "swap_usage_percentage": swap.percent,
                "total_memory_gb": memory.total / (1024 ** 3),
                "available_memory_gb": memory.available / (1024 ** 3),
            },
            "additional_info": {
                "collection_timestamp": time.time(),
                "performance_concern": "High memory usage detected"
                if memory.percent > 80
                else None,
                "swap_concern": "High swap usage detected" if swap.percent > 80 else None,
            },
        }

    except Exception as e:
        return {
            "result": {"error": f"Failed to gather memory information: {str(e)}"},
            "stats": {"success": False},
        }