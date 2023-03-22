import logging
import os

from dotenv import load_dotenv
from slack_sdk import WebClient

from src.models.form import SlackForm
from src.models.schedule import FormSchedule, ScheduledEvent
from src import slack_ui_blocks
from src import slack_actions

load_dotenv()
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


__all__ = ['schedule_slack_message', 'delete_slack_scheduled_message']


def schedule_slack_message(schedule: FormSchedule, event: ScheduledEvent):
    form = SlackForm.objects(id=schedule.form_id).first()
    blocks = slack_ui_blocks.form_slack_ui_blocks(form, action_id=slack_actions.SUBMIT_FORM_SCHEDULED)
    result = client.chat_scheduleMessage(
        channel=schedule.user_id,
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