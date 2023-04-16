import os

from src.models.form import SlackForm
from src.models.schedule import FormSchedule
from src.slack_api.slack_user import SlackUser
from src.slack_ui.blocks import text_block_item, divider_block, form_list_item, form_list_item_action_buttons
from src.slack_ui.text import no_forms_text


def list_of_forms_blocks(user: SlackUser):
    """
    Slack UI blocks with a list of Forms
    """
    forms = SlackForm.objects(user_id=user.id)
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
        if i < forms.count():
            blocks.append(divider_block)
    return blocks
