"""Pure helpers for the persistent report scheduler."""
from datetime import datetime, timedelta
from typing import Any, Dict


def schedule_slot_is_due(slot: Dict[str, Any], now: datetime, catch_up_minutes: int = 120) -> bool:
    """Return whether an enabled schedule should run now, including a safe late-start window."""
    if not slot.get("is_enabled", 1):
        return False
    if str(slot.get("last_run") or "").startswith(now.strftime("%Y-%m-%d")):
        return False
    try:
        scheduled_time = datetime.strptime(str(slot.get("run_time") or ""), "%H:%M").time()
    except ValueError:
        return False

    scheduled_at = now.replace(
        hour=scheduled_time.hour,
        minute=scheduled_time.minute,
        second=0,
        microsecond=0,
    )
    return timedelta(0) <= now - scheduled_at <= timedelta(minutes=catch_up_minutes)
