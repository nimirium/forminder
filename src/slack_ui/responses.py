from src.slack_ui.blocks import text_block_item
from src.slack_ui.elements import view_submissions_button
from src.slack_ui.text import help_text


def text_response(text):
    return {
        "blocks": [text_block_item(text)]
    }


help_text_response = {
    "blocks": [text_block_item(help_text)]
}


def form_was_submitted_response(form_id):
    return {
        "blocks": [
            text_block_item(":herb: The form was submitted :herb:"),
            {
                "type": "actions",
                "elements": [
                    view_submissions_button(form_id),
                ]
            },
        ]
    }
