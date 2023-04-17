import datetime
import logging
import time

from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError

from src.models.connect import connect_to_mongo
from src.models.schedule import FormSchedule, ScheduledEvent
from src.services.slack_scheduler_service import schedule_slack_message, handle_forminder_not_in_channel
from src.slack_api.slack_client import get_slack_client

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
client = get_slack_client()


def schedule_future_messages():
    st = time.perf_counter()
    logging.info("Scheduling slack messages...")
    for schedule in FormSchedule.objects.all():
        for event in schedule.get_events_to_schedule(days=7):
            try:
                slack_message_id = schedule_slack_message(schedule, event)
                event.slack_message_id = slack_message_id
                event.save()
                logging.info(f"scheduled slack message for {event.execution_time_utc}")
            except SlackApiError as e:
                if e.response.data['error'] == 'not_in_channel':
                    handle_forminder_not_in_channel(schedule, event)
                else:
                    raise e

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
