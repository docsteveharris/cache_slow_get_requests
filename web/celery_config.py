# from web.tasks import get_response
from web.app import slow_url

beat_schedule = {
    "get_slow_url": {"task": "web.tasks.get_response", "schedule": 10.0, "args": (slow_url, "slow_url")}
}

task_time_limit = 600
task_track_started = True

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

imports = ("web.tasks",)

beat_schedule_filename = "celerybeat-schedule"
