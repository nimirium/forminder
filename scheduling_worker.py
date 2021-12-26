import logging

from models.connect import connect_to_mongo
from models.schedule import SlackFormSchedule
from util import slack_scheduler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_scheduling_worker():
    for schedule in SlackFormSchedule.objects.all():
        for event in schedule.get_events_to_schedule(days=7):
            scheduled_message_id = slack_scheduler.schedule_slack_message(schedule, event)
            event.scheduled_message_id = scheduled_message_id
            event.save()
            logging.info(f"scheduled slack message for {event.execution_time_utc}")


if __name__ == '__main__':
    connect_to_mongo()
    run_scheduling_worker()
