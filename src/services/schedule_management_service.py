import json
import logging
from threading import Thread

import requests as requests
from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError

from src import constants
from src.services.list_of_forms import list_of_forms_blocks
from src.services.slack_scheduler_service import schedule_slack_message, delete_slack_scheduled_message, \
    handle_forminder_not_in_channel
from src.slack_ui import blocks as slack_ui_blocks, responses as slack_ui_responses
from src.models.form import SlackForm
from src.models.schedule import FormSchedule, TimeField, ScheduledEvent
from src.slack_api.slack_client import get_slack_client
from src.slack_api.slack_user import SlackUser
from src.utils import DAYS_OF_THE_WEEK

load_dotenv()
client = get_slack_client()


def reminder_select(form, validation_error: str = None):
    channels_response = client.conversations_list()
    send_to_options = ['me'] + ['#' + x['name'] for x in channels_response['channels']]
    return slack_ui_blocks.reminder_select_block(form, send_to_options, validation_error)

def schedule_form_command(form_id, user, response_url):
    Thread(target=send_schedule_form_response, kwargs=dict(form_id=form_id, user=user, response_url=response_url)).start()
    return


def send_schedule_form_response(form_id, user: SlackUser, response_url):
    form = SlackForm.objects(team_id=user.team_id, id=form_id).first()
    result = reminder_select(form)
    requests.post(response_url, json.dumps(result))


def create_form_schedule_command(form_id, user: SlackUser, schedule_form_state, response_url):
    days_of_the_week = []
    at_time = None
    send_to = None
    for part in schedule_form_state.values():
        if part.get(constants.SEND_SCHEDULE_TO):
            send_to = part[constants.SEND_SCHEDULE_TO]['selected_option']['value']
            if send_to == 'me':
                send_to = user.id
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
    form = SlackForm.objects(team_id=user.team_id, id=form_id).first()
    if send_to is None:
        result = reminder_select(form, validation_error="*Please select message target*")
        return requests.post(response_url, json.dumps(result))
    if len(days_of_the_week) == 0:
        result = reminder_select(form, validation_error="*Please select weekdays*")
        return requests.post(response_url, json.dumps(result))

    if not at_time:
        at_time = constants.DEFAULT_SCHEDULE_TIME
    hour = int(at_time.split(':')[0])
    minute = int(at_time.split(':')[1])
    time_local = TimeField(hour=hour, minute=minute)
    existing = FormSchedule.objects(user_id=user.id, form_id=form_id, days_of_the_week=days_of_the_week,
                                    timezone=user.tz, time_local=time_local)
    if existing.count() > 0:
        result = slack_ui_responses.text_response(":warning: This schedule already exists! :warning:")
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
        scheduled_message_id = schedule_slack_message(schedule, next_event)
    except Exception as e:
        if isinstance(e, SlackApiError) and e.response.data['error'] == 'not_in_channel':
            handle_forminder_not_in_channel(schedule, next_event)
            return requests.post(response_url, json.dumps(
                slack_ui_responses.text_response(f":warning: Schedule was created, but Forminder must be part of "
                                                 f"{schedule.send_to} for the schedule to work.\n"
                                                 f":warning: Please invite Forminder to {schedule.send_to}.")))
        else:
            logging.exception(f"Error in schedule_slack_message: {schedule=}, {next_event=}")
            next_event.delete()
            schedule.delete()
            return requests.post(response_url, json.dumps(
                slack_ui_responses.text_response(":x: Failed to create schedule :x:")))

    next_event.scheduled_message_id = scheduled_message_id
    next_event.save()

    result = slack_ui_responses.text_response(f":clock3: Schedule was created :clock3:\n"
                                              f"Forminder will remind {schedule.send_to_name()} to fill '{form.name}' "
                                              f"on {schedule.schedule_description()}")
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
        blocks = list_of_forms_blocks(user)
        response = dict(blocks=[result, slack_ui_blocks.divider_block] + blocks)
        requests.post(response_url, json.dumps(response))
        return
    logging.warning(f"can't delete schedule {schedule_id} because it doesn't exist")
    result = slack_ui_responses.text_response(":x: Failed to delete schedule :x:")
    requests.post(response_url, json.dumps(result))
