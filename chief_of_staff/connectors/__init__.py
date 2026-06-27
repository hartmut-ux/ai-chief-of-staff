"""Source connectors."""

from .calendar import fetch_calendar
from .custom import fetch_custom
from .email import fetch_email
from .tasks import fetch_tasks
from .web import fetch_web


FETCHERS = {
    "email": fetch_email,
    "calendar": fetch_calendar,
    "tasks": fetch_tasks,
    "web": fetch_web,
    "custom": fetch_custom,
}
