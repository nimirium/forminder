import logging

from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError

from src import constants
from src.slack_ui import blocks as slack_ui_blocks
from src.models.form import SlackForm
from src.models.schedule import FormSchedule, ScheduledEvent
from src.slack_api.slack_client import get_slack_client

load_dotenv()
client = get_slack_client()


def schedule_slack_message(schedule: FormSchedule, event: ScheduledEvent):
    """
    Schedules a message to be sent to slack for a specific time.
    The message itself is the reminder to fill the form.
    :return: Scheduled message ID in slack
    """
    form = SlackForm.objects(id=schedule.form_id).first()
    blocks = slack_ui_blocks.form_slack_ui_blocks(form, action_id=constants.SUBMIT_FORM_SCHEDULED)
    result = client.chat_scheduleMessage(
        channel=schedule.send_to,
        text="Hi! It's time to fill a form",
        blocks=blocks,
        post_at=int(event.execution_time_utc.timestamp()),
    )
    logging.info(result)
    logging.info("created slack schedule")
    return result.data['scheduled_message_id']


def delete_slack_scheduled_message(user_id, slack_message_id):
    result = client.chat_deleteScheduledMessage(
        channel=user_id,
        scheduled_message_id=slack_message_id,
    )
    logging.info(result)
    logging.info("deleted slack schedule")


def handle_forminder_not_in_channel(schedule, event):
    logging.warning(f"Forminder is not part of channel {schedule.send_to}, can't schedule message. "
                    f"Instead, sending a message to the schedule creator {schedule.user_name}")
    try:
        result = client.chat_scheduleMessage(
            channel=schedule.user_id,
            text=f"Hi! You created a schedule to send a form to {schedule.send_to} channel. For this to "
                 f"work please invite Forminder to {schedule.send_to}",
            post_at=int(event.execution_time_utc.timestamp()),
        )
        logging.info(result)
    except SlackApiError:
        logging.exception("Couldn't inform user that they must invite Forminder to channel")
