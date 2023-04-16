import os

import math

from src.models.form import SlackForm
from src.models.schedule import FormSchedule
from src.slack_api.slack_user import SlackUser
from src.slack_ui.blocks import text_block_item, divider_block, form_list_item, form_list_item_action_buttons, \
    pagination_buttons_block
from src.slack_ui.text import no_forms_text


def list_of_forms_blocks(user: SlackUser, page: int = 1, items_per_page: int = 5):
    """
    Slack UI blocks with a list of Forms
    """
    forms = SlackForm.objects(user_id=user.id)
    total_forms = forms.count()

    if total_forms == 0:
        return [text_block_item(no_forms_text)]

    start = (page - 1) * items_per_page
    end = start + items_per_page
    forms = forms[start:end]
    if forms.count() == 0:
        return [text_block_item(no_forms_text)]
    blocks = [text_block_item(
        f"*List of forms* <{os.environ['DOMAIN']}/forms|[View in the Forminder website]>"), divider_block]
    for i, form in enumerate(forms):
        schedules = FormSchedule.objects(form_id=str(form.id))
        for block in form_list_item(form, schedules):
            blocks.append(block)
        can_delete = form.user_id == user.id or user.is_admin
        blocks.append(form_list_item_action_buttons(str(form.id), can_delete))
        blocks.append(divider_block)
    total_pages = math.ceil(total_forms / items_per_page)
    blocks.append(text_block_item(f"Page {page} out of {total_pages}"))
    pagination_block = pagination_buttons_block(page, total_forms, items_per_page)
    if pagination_block:
        blocks.append(pagination_block)
    return blocks
