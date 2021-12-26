from mongoengine import Q

from models.form import SlackForm
from models.schedule import SlackFormSchedule
from util import slack_blocks


def list_form_blocks(user_id):
    blocks = [slack_blocks.text_block_item("*List of forms:*"), slack_blocks.divider]
    forms = SlackForm.objects(Q(user_id=user_id) or Q(public=True))
    for i, form in enumerate(forms):
        schedules = SlackFormSchedule.objects(form_id=str(form.id))
        for block in slack_blocks.form_list_item(form, schedules):
            blocks.append(block)
        blocks.append(slack_blocks.form_list_item_action_buttons(str(form.id)))
        if i < forms.count():
            blocks.append(slack_blocks.divider)
    return blocks
