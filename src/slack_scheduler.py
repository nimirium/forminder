import logging

from dotenv import load_dotenv

from src import constants
from src.slack_ui import blocks as slack_ui_blocks
from src.models.form import SlackForm
from src.models.schedule import FormSchedule, ScheduledEvent
from src.slack_api.slack_client import get_slack_client

load_dotenv()
client = get_slack_client()


__all__ = ['schedule_slack_message', 'delete_slack_scheduled_message']


def schedule_slack_message(schedule: FormSchedule, event: ScheduledEvent):
    form = SlackForm.objects(id=schedule.form_id).first()
    blocks = slack_ui_blocks.form_slack_ui_blocks(form, action_id=constants.SUBMIT_FORM_SCHEDULED)
    result = client.chat_scheduleMessage(
        channel=schedule.user_id if schedule.send_to.lower().strip() == 'me' else schedule.send_to,
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