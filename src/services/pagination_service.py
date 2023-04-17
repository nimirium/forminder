import math

from src import constants
from src.models.form import SlackForm
from src.services import forms_service


def handle_pagination(prefix, page_button, user, response_url, current_page):
    if prefix == constants.LIST_FORMS_PREFIX:
        if page_button == constants.FIRST_PAGE:
            return forms_service.list_forms_command(user, response_url, 1)
        elif page_button == constants.PREVIOUS_PAGE:
            return forms_service.list_forms_command(user, response_url, current_page - 1)
        elif page_button == constants.NEXT_PAGE:
            return forms_service.list_forms_command(user, response_url, current_page + 1)
        elif page_button == constants.LAST_PAGE:
            total_forms = SlackForm.objects(team_id=user.team_id).count()
            last_page = math.ceil(total_forms / constants.FORM_ITEMS_PER_PAGE)
            return forms_service.list_forms_command(user, response_url, last_page)
    elif prefix == constants.FILL_FORMS_PREFIX:
        if page_button == constants.FIRST_PAGE:
            return forms_service.fill_form_command(user, [], response_url, page=1)
        elif page_button == constants.PREVIOUS_PAGE:
            return forms_service.fill_form_command(user, [], response_url, page=current_page - 1)
        elif page_button == constants.NEXT_PAGE:
            return forms_service.fill_form_command(user, [], response_url, page=current_page + 1)
        elif page_button == constants.LAST_PAGE:
            total_forms = SlackForm.objects.filter(team_id=user.team_id).count()
            items_per_page = 5
            last_page = math.ceil(total_forms / items_per_page)
            return forms_service.fill_form_command(user, [], response_url, page=last_page)
