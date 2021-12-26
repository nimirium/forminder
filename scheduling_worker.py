import datetime
import logging
import os
import time

from dotenv import load_dotenv
from slack_sdk import WebClient

from models.connect import connect_to_mongo
from models.schedule import SlackFormSchedule, ScheduledEvent
from util import slack_scheduler

logging.getLogger().setLevel(logging.INFO)

load_dotenv()
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def schedule_future_messages():
    st = time.perf_counter()
    logging.info("Scheduling slack messages...")
    for schedule in SlackFormSchedule.objects.all():
        for event in schedule.get_events_to_schedule(days=7):
            slack_message_id = slack_scheduler.schedule_slack_message(schedule, event)
            event.slack_message_id = slack_message_id
            event.save()
            logging.info(f"scheduled slack message for {event.execution_time_utc}")
    logging.info(f"Done scheduling slack messages, it took {time.perf_counter() - st}")


def clear_scheduled_messages():
    logging.info("Clearing slack messages...")
    now = datetime.datetime.now(datetime.timezone.utc)
    latest = now + datetime.timedelta(days=7)
    result = client.chat_scheduledMessages_list(
        oldest=str(int(now.timestamp())),
        latest=str(int(latest.timestamp())),
    )
    for message in result["scheduled_messages"]:
        logging.info(message)
        event = ScheduledEvent.objects(slack_message_id=message['id']).first()
        if not event:
            logging.info(f"deleting scheduled message {message['id']}")
            client.chat_deleteScheduledMessage(scheduled_message_id=message['id'], channel=message['channel_id'])


def run_scheduling_worker():
    schedule_future_messages()
    clear_scheduled_messages()


if __name__ == '__main__':
    connect_to_mongo()
    run_scheduling_worker()
