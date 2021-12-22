from random import randint

__all__ = ['text_response', 'help_text_block', 'random_skin_tone', 'form_create_help_text']

DAYS_OF_THE_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def random_skin_tone():
    return f":skin-tone-{randint(1, 6)}:"


def text_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def text_response(text):
    return {
        "blocks": [text_block(text)]
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


def checkboxes_block(title, options):
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
            "action_id": "checkboxes-action"
        }
    }


def time_picker_block(title, initial_time):
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
            "action_id": "timepicker-action"
        }
    }


reminder_select_block = {
    "blocks": [
        header_block("Hi! When would you like to be reminded to fill the form?"),
        checkboxes_block("When do you want to be notified?", DAYS_OF_THE_WEEK),
        time_picker_block("At", "09:00"),
    ]
}

help_text = f""":information_desk_person:{random_skin_tone()} Usage:
:one: /ask-remind create-form
:two: /ask-remind schedule
:three: /ask-remind list forms
:four: /ask-remind list schedules"""

help_text_block = {
    "blocks": [text_block(help_text)]
}

form_create_help_text = f""":information_desk_person:{random_skin_tone()} create-form usage:
/ask-remind create-form --form-name=“My Form” --text=“Name” --text=“Age” --text-multiline=“Hobbies”
--form-name is the name of the form
--text adds a text field to the form
--text-multiline adds a multi-line text field to the form
--public use this to make your form public, otherwise it will only be available to you
"""
