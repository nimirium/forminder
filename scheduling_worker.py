import datetime
import logging
import os
import time

from dotenv import load_dotenv
from slack_sdk import WebClient

from src.models.connect import connect_to_mongo
from src.models.schedule import FormSchedule, ScheduledEvent
from src import slack_scheduler

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def schedule_future_messages():
    st = time.perf_counter()
    logging.info("Scheduling slack messages...")
    for schedule in FormSchedule.objects.all():
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
    while True:
        st = time.time()
        schedule_future_messages()
        clear_scheduled_messages()
        sleep_time = 60 - (time.time() - st)
        if sleep_time > 0:
            logging.info("sleeping for {:.2f} seconds".format(sleep_time))
            time.sleep(sleep_time)


def main():
    connect_to_mongo()
    run_scheduling_worker()


if __name__ == '__main__':
    main()
