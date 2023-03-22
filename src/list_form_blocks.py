from mongoengine import Q

from src.models.form import SlackForm
from src.models.schedule import FormSchedule
from src import slack_ui_blocks
from src.slack_ui_blocks import random_skin_tone


def _no_forms_text():
    return f""":information_desk_person:{random_skin_tone()} There are no forms yet
:information_source: use “/forminder create” to create one"""


def list_form_blocks(user_id):
    forms = SlackForm.objects(Q(user_id=user_id) or Q(public=True))
    if forms.count() == 0:
        return [slack_ui_blocks.text_block_item(_no_forms_text())]
    blocks = [slack_ui_blocks.text_block_item("*List of forms:*"), slack_ui_blocks.divider]
    for i, form in enumerate(forms):
        schedules = FormSchedule.objects(form_id=str(form.id))
        for block in slack_ui_blocks.form_list_item(form, schedules):
            blocks.append(block)
        blocks.append(slack_ui_blocks.form_list_item_action_buttons(str(form.id)))
        if i < forms.count():
            blocks.append(slack_ui_blocks.divider)
    return blocks
