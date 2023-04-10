import json
import logging
from threading import Thread

import requests as requests
from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError

from src import constants, slack_scheduler
from src import slack_ui_blocks
from src.list_form_blocks import list_form_blocks
from src.models.form import SlackForm
from src.models.schedule import FormSchedule, TimeField, ScheduledEvent
from src.slack_api.slack_client import get_slack_client, get_users_tz
from src.slack_api.slack_user import SlackUser
from src.slack_scheduler import delete_slack_scheduled_message
from src.utils import DAYS_OF_THE_WEEK

load_dotenv()
client = get_slack_client()


def schedule_form_command(form_id, response_url):
    Thread(target=send_schedule_form_response, kwargs=dict(form_id=form_id, response_url=response_url)).start()
    return


def send_schedule_form_response(form_id, response_url):
    channels_response = client.conversations_list()
    send_to_options = ['me'] + ['#' + x['name'] for x in channels_response['channels']]
    result = slack_ui_blocks.reminder_select_block(form_id, send_to_options)
    requests.post(response_url, json.dumps(result))


def create_form_schedule_command(form_id, user: SlackUser, schedule_form_state, response_url):
    days_of_the_week = []
    at_time = None
    send_to = None
    for part in schedule_form_state.values():
        if part.get(constants.SEND_SCHEDULE_TO):
            send_to = part[constants.SEND_SCHEDULE_TO]['selected_option']['value']
        if part.get(constants.FORM_WEEKDAYS):
            for selected_option in part[constants.FORM_WEEKDAYS]['selected_options']:
                weekday_number = DAYS_OF_THE_WEEK.index(selected_option['value'])
                days_of_the_week.append(weekday_number)
        elif part.get(constants.FORM_TIME):
            at_time = part[constants.FORM_TIME]['selected_time']
    Thread(target=create_schedule_and_respond,
           kwargs=dict(form_id=form_id, user=user, days_of_the_week=days_of_the_week,
                       at_time=at_time, send_to=send_to, response_url=response_url)).start()
    return


def create_schedule_and_respond(form_id, user: SlackUser, days_of_the_week, at_time, send_to, response_url):
    hour = int(at_time.split(':')[0])
    minute = int(at_time.split(':')[1])
    time_local = TimeField(hour=hour, minute=minute)
    existing = FormSchedule.objects(user_id=user.id, form_id=form_id, days_of_the_week=days_of_the_week,
                                    timezone=user.tz, time_local=time_local)
    if existing.count() > 0:
        result = slack_ui_blocks.text_response(":warning: This schedule already exists! :warning:")
        return requests.post(response_url, json.dumps(result))
    schedule = FormSchedule(
        user_id=user.id,
        user_name=user.username,
        form_id=form_id,
        days_of_the_week=days_of_the_week,
        send_to=send_to,
        timezone=user.tz,
        time_local=time_local,
    )
    next_event = schedule.save_and_schedule_next()
    try:
        scheduled_message_id = slack_scheduler.schedule_slack_message(schedule, next_event)
    except Exception as e:
        logging.exception(f"Error fetching slack users_info: {schedule=}, {next_event=}")
        next_event.delete()
        schedule.delete()
        if isinstance(e, SlackApiError):
            return requests.post(response_url, json.dumps(slack_ui_blocks.text_response(":x: Failed to create schedule :x:")))
        else:
            return requests.post(response_url, json.dumps(slack_ui_blocks.text_response(":x: Failed to create schedule :x:")))

    next_event.scheduled_message_id = scheduled_message_id
    next_event.save()

    result = slack_ui_blocks.text_response(":clock3: Schedule was created :clock3:")
    requests.post(response_url, json.dumps(result))


def delete_schedule_command(schedule_id, user, response_url):
    Thread(target=delete_schedule_and_respond,
           kwargs=dict(schedule_id=schedule_id, user_id=user, response_url=response_url)).start()
    return


def delete_schedule_and_respond(schedule_id, user, response_url):
    schedule = FormSchedule.objects(id=schedule_id).first()
    if schedule:
        form = SlackForm.objects(id=schedule.form_id).first()
        for event in ScheduledEvent.objects(schedule=schedule):
            if event.slack_message_id:
                delete_slack_scheduled_message(schedule.user_id, event.slack_message_id)
            event.delete()
        schedule.delete()
        result = slack_ui_blocks.text_block_item(f":white_check_mark: Deleted schedule for {form.name} form - "
                                              f"{schedule.schedule_description()}")
        blocks = list_form_blocks(user)
        response = dict(blocks=[result, slack_ui_blocks.divider] + blocks)
        requests.post(response_url, json.dumps(response))
        return
    logging.warning(f"can't delete schedule {schedule_id} because it doesn't exist")
    result = slack_ui_blocks.text_response(":x: Failed to delete schedule :x:")
    requests.post(response_url, json.dumps(result))
