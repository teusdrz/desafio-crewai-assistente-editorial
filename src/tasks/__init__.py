"""
Tasks Package
"""

from .editorial_tasks import (
    create_book_details_task,
    create_store_finder_task,
    create_support_ticket_task,
    create_intent_detection_task
)

__all__ = [
    "create_book_details_task",
    "create_store_finder_task",
    "create_support_ticket_task", 
    "create_intent_detection_task"
]
