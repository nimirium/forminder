from typing import List, Dict

import math

from src import constants
from src.slack_ui.elements import button_element, view_submissions_button_element
from src.utils import DAYS_OF_THE_WEEK

divider_block = {
    "type": "divider"
}


def text_block_item(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def header_block(title):
    return {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": title,
            "emoji": True
        }
    }


def checkboxes_block(title, options, action_id):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": title
        },
        "accessory": {
            "type": "checkboxes",
            "options": [
                {
                    "text": {
                        "type": "mrkdwn",
                        "text": option
                    },
                    "value": option
                } for option in options
            ],
            "action_id": action_id,
        }
    }


def time_picker_block(title, initial_time, action_id):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": title,
        },
        "accessory": {
            "type": "timepicker",
            "initial_time": initial_time,
            "placeholder": {
                "type": "plain_text",
                "text": "Select time",
                "emoji": True
            },
            "action_id": action_id
        }
    }


def button_block(text, value, action_id):
    return {
        "type": "actions",
        "elements": [
            button_element(text, value, action_id),
        ]
    }


def actions_block(button_elements: List[Dict]):
    return {
        "type": "actions",
        "elements": button_elements
    }


def reminder_select_block(form_id, send_to_options):
    return {
        "blocks": [
            select_block("Send a message to: ", send_to_options, action=constants.SEND_SCHEDULE_TO),
            checkboxes_block("When would you like to be reminded to fill the form?", DAYS_OF_THE_WEEK,
                             constants.FORM_WEEKDAYS),
            time_picker_block("At", "09:00", constants.FORM_TIME),
            button_block(text="Send", value=form_id, action_id=constants.CREATE_FORM_SCHEDULE),
        ]
    }


def form_list_item_action_buttons(form_id, can_delete):
    result = {
        "type": "actions",
        "elements": [
            button_element("Schedule", form_id, constants.SCHEDULE_FORM),
            button_element("Fill now", form_id, constants.FILL_FORM_NOW),
            view_submissions_button_element(form_id),
        ]
    }
    if can_delete:
        result['elements'].append(button_element("Delete Form", form_id, constants.DELETE_FORM))
    return result


def text_and_button(text, button_text, value, action_id):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },
        "accessory": button_element(button_text, value, action_id),
    }


def form_list_item(form, schedules):
    fields_description = ', '.join([f"{f.title} ({f.type})" for f in form.fields])
    blocks = [
        text_block_item(f":page_with_curl: {form.name}"),
        text_block_item(f"Fields: {fields_description}"),
    ]
    if schedules.count() == 0:
        blocks.append(text_block_item("Not scheduled"))
    else:
        blocks.append(text_block_item("Scheduled for:"))
        for schedule in schedules:
            text = "- " + schedule.schedule_description()
            blocks.append(text_and_button(text, "Delete Schedule", str(schedule.id), constants.DELETE_SCHEDULE))
    return blocks


def text_input_block(title, action, multiline=False):
    return {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "multiline": multiline,
            "action_id": action,
        },
        "label": {
            "type": "plain_text",
            "text": title,
            "emoji": True
        }
    }


def select_block(title, options, action):
    return {
        "type": "section",
        "block_id": f"section-{action}",
        "text": {
            "type": "mrkdwn",
            "text": title
        },
        "accessory": {
            "action_id": action,
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select an item"
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": option
                    },
                    "value": option
                } for option in options
            ]
        }
    }


def select_channel_block():
    return {
        "type": "section",
        "block_id": "section678",
        "text": {
            "type": "mrkdwn",
            "text": "Pick channels from the list"
        },
        "accessory": {
            "action_id": "text1234",
            "type": "multi_channels_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select channels"
            }
        }
    }



def form_slack_ui_blocks(form, action_id):
    blocks = [
        text_block_item(form.name),
    ]
    for field in form.fields:
        if field.type == 'text':
            blocks.append(text_input_block(field.title, action=str(field.id), multiline=False))
        elif field.type == 'text-multiline':
            blocks.append(text_input_block(field.title, action=str(field.id), multiline=True))
        elif field.type == 'select':
            blocks.append(select_block(field.title, field.options, action=str(field.id)))
    blocks.append(button_block(text="Submit", value=str(form.id), action_id=action_id))
    return blocks


def select_form_to_fill(forms, title="*Select a form to fill*"):
    ##3

    ###
    blocks = [
        text_block_item(title),
    ]
    for i, form in enumerate(forms):
        fields_description = ', '.join([f"{f.title} ({f.type})" for f in form.fields])
        blocks.extend([
            text_block_item(f":page_with_curl: {form.name}"),
            text_block_item(f"Fields: {fields_description}"),
            button_block("Fill now", str(form.id), constants.FILL_FORM_NOW),
        ])
        if i < len(forms) - 1:
            blocks.append(divider_block)
    return {"blocks":  blocks}


def pagination_buttons_block(current_page: int, total_items: int, items_per_page: int):
    total_pages = math.ceil(total_items / items_per_page)
    previous_visible = current_page > 1
    next_visible = current_page < total_pages
    buttons = []

    if previous_visible:
        buttons.append({
            "type": "button",
            "text": {"type": "plain_text", "text": "Previous page", "emoji": True},
            "value": "prev_page",
            "action_id": constants.LIST_FORMS_PREVIOUS_PAGE,
        })

    if next_visible:
        buttons.append({
            "type": "button",
            "text": {"type": "plain_text", "text": "Next page", "emoji": True},
            "value": "next_page",
            "action_id": constants.LIST_FORMS_NEXT_PAGE,
        })

    if not buttons:
        return None

    return {
        "type": "actions",
        "block_id": f"pagination:{current_page}",
        "elements": buttons
    }
