import os

from src import constants


def button_element(text, value, action_id):
    return {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True
        },
        "value": value,
        "action_id": action_id
    }


def button_url_element(text, value, url, action_id):
    return {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True
        },
        "value": value,
        "url": url,
        "action_id": action_id,
    }


def view_submissions_button(form_id):
    return button_url_element(text="View submissions", value=form_id,
                              url=f"{os.environ['DOMAIN']}/submissions?formId={form_id}",
                              action_id=constants.VIEW_FORM_SUBMISSIONS)
