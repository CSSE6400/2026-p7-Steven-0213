import os
import time
import datetime
import icalendar
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.task_default_queue = os.environ.get("CELERY_DEFAULT_QUEUE", "ical")

@celery.task(name="ical")
def create_ical(tasks):
    cal = icalendar.Calendar()
    cal.add("prodid", "-//Taskoverflow Calendar//mxm.dk//")
    cal.add("version", "2.0")

    time.sleep(5)

    for task in tasks:
        event = icalendar.Event()
        event.add("uid", task["id"])
        event.add("summary", task["title"])
        event.add("description", task["description"])

        deadline = task.get("deadline_at")
        if deadline:
            deadline = deadline.replace("Z", "")
            try:
                dt = datetime.datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                dt = datetime.datetime.fromisoformat(deadline)
            event.add("dtstart", dt)

        cal.add_component(event)

    return cal.to_ical().decode("utf-8")