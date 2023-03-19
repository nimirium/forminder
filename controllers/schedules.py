import json
import logging
import os
from threading import Thread

import requests as requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

from controllers.shared import list_form_blocks
from models.form import SlackForm
from models.schedule import FormSchedule, TimeField, ScheduledEvent
from util import slack_blocks, slack_scheduler, slack_actions
from util.slack_scheduler import delete_slack_scheduled_message
from util.utils import DAYS_OF_THE_WEEK

load_dotenv()
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def schedule_form_command(form_id, response_url):
    Thread(target=_send_schedule_form_response, kwargs=dict(form_id=form_id, response_url=response_url)).start()
    return


def _send_schedule_form_response(form_id, response_url):
    result = slack_blocks.reminder_select_block(form_id)
    requests.post(response_url, json.dumps(result))


def create_form_schedule_command(form_id, user_id, user_name, schedule_form_state, response_url):
    days_of_the_week = []
    at_time = None
    for part in schedule_form_state.values():
        if part.get(slack_actions.FORM_WEEKDAYS):
            for selected_option in part[slack_actions.FORM_WEEKDAYS]['selected_options']:
                weekday_number = DAYS_OF_THE_WEEK.index(selected_option['value'])
                days_of_the_week.append(weekday_number)
        elif part.get(slack_actions.FORM_TIME):
            at_time = part[slack_actions.FORM_TIME]['selected_time']
    Thread(target=_create_schedule_and_respond,
           kwargs=dict(form_id=form_id, user_id=user_id, user_name=user_name, days_of_the_week=days_of_the_week,
                       at_time=at_time, response_url=response_url)).start()
    return


def _create_schedule_and_respond(form_id, user_id, user_name, days_of_the_week, at_time, response_url):
    try:
        result = client.users_info(user=user_id)
        logging.info(result)
    except SlackApiError as e:
        logging.error("Error fetching conversations: {}".format(e))
        return slack_blocks.text_response(":x: Failed to create schedule :x:")
    tz_name = result.data['user']['tz']
    hour = int(at_time.split(':')[0])
    minute = int(at_time.split(':')[1])
    time_local = TimeField(hour=hour, minute=minute)
    existing = FormSchedule.objects(user_id=user_id, form_id=form_id, days_of_the_week=days_of_the_week,
                                    timezone=tz_name, time_local=time_local)
    if existing.count() > 0:
        result = slack_blocks.text_response(":warning: This schedule already exists! :warning:")
        requests.post(response_url, json.dumps(result))
        return
    schedule = FormSchedule(
        user_id=user_id,
        user_name=user_name,
        form_id=form_id,
        days_of_the_week=days_of_the_week,
        timezone=tz_name,
        time_local=time_local,
    )
    next_event = schedule.save_and_schedule_next()
    try:
        scheduled_message_id = slack_scheduler.schedule_slack_message(schedule, next_event)
    except Exception as e:
        next_event.delete()
        schedule.delete()
        return slack_blocks.text_response(":x: Failed to create schedule :x:")

    next_event.scheduled_message_id = scheduled_message_id
    next_event.save()

    result = slack_blocks.text_response(":clock3: Schedule was created :clock3:")
    requests.post(response_url, json.dumps(result))


def delete_schedule_command(schedule_id, user_id, response_url):
    Thread(target=_delete_schedule_and_respond,
           kwargs=dict(schedule_id=schedule_id, user_id=user_id, response_url=response_url)).start()
    return


def _delete_schedule_and_respond(schedule_id, user_id, response_url):
    schedule = FormSchedule.objects(id=schedule_id).first()
    if schedule:
        form = SlackForm.objects(id=schedule.form_id).first()
        for event in ScheduledEvent.objects(schedule=schedule):
            if event.slack_message_id:
                delete_slack_scheduled_message(schedule.user_id, event.slack_message_id)
            event.delete()
        schedule.delete()
        result = slack_blocks.text_block_item(f":white_check_mark: Deleted schedule for {form.name} form - "
                                              f"{schedule.schedule_description()}")
        blocks = list_form_blocks(user_id)
        response = dict(blocks=[result, slack_blocks.divider] + blocks)
        requests.post(response_url, json.dumps(response))
        return
    logging.warning(f"can't delete schedule {schedule_id} because it doesn't exist")
    result = slack_blocks.text_response(":x: Failed to delete schedule :x:")
    requests.post(response_url, json.dumps(result))
