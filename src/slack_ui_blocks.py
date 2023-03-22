from random import randint

__all__ = ['text_response', 'help_text_block', 'random_skin_tone', 'form_create_help_text', 'text_block_item']

from src import slack_actions
from src.utils import DAYS_OF_THE_WEEK


def random_skin_tone():
    tone = randint(1, 6)
    return '' if tone == 1 else f":skin-tone-{tone}:"


divider = {
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


def text_response(text):
    return {
        "blocks": [text_block_item(text)]
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
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": text,
                    "emoji": True
                },
                "value": value,
                "action_id": action_id
            }
        ]
    }


def reminder_select_block(form_id):
    return {
        "blocks": [
            # select_block("PM in a", ["Slack channel", "Personal message"], action=slack_actions.SEND_SCHEDULE_TO),
            checkboxes_block("When would you like to be reminded to fill the form?", DAYS_OF_THE_WEEK,
                             slack_actions.FORM_WEEKDAYS),
            time_picker_block("At", "09:00", slack_actions.FORM_TIME),
            button_block(text="Send", value=form_id, action_id=slack_actions.CREATE_FORM_SCHEDULE),
        ]
    }


help_text = f""":information_desk_person:{random_skin_tone()} Usage:
:one: /forminder create
:two: /forminder list"""

help_text_block = {
    "blocks": [text_block_item(help_text)]
}

form_create_help_text = f""":information_desk_person:{random_skin_tone()} create-form usage:
```/forminder create --form-name="My Form" --text-field="First name" --text-field="Last name" --multiline-field="Hobbies" --select-field="Color:blue,red,yellow" --public```
`--form-name` - Required, the name of the form
`--text-field` - Optional, adds a text field to the form
`--multiline-field` - Optional, adds a multi-line text field to the form
`--select-field` - Optional, adds a select field to the form
`--public` Optional, use this to make your form public, otherwise it will only be available to you
"""


def form_list_item_action_buttons(form_id):
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Fill now",
                    "emoji": True
                },
                "value": form_id,
                "action_id": slack_actions.FILL_FORM_NOW,
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "View submissions",
                    "emoji": True
                },
                "value": form_id,
                "action_id": slack_actions.VIEW_FORM_SUBMISSIONS,
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Schedule",
                    "emoji": True
                },
                "value": form_id,
                "action_id": slack_actions.SCHEDULE_FORM,
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Delete Form",
                    "emoji": True
                },
                "value": form_id,
                "action_id": slack_actions.DELETE_FORM,
            }
        ]
    }


def text_and_button(text, button_text, value, action_id):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": button_text,
                "emoji": True
            },
            "value": value,
            "action_id": action_id
        }
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
            blocks.append(text_and_button(text, "Delete Schedule", str(schedule.id), slack_actions.DELETE_SCHEDULE))
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
