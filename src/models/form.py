import datetime

from mongoengine import Document, StringField, EmbeddedDocument, ListField, EmbeddedDocumentField, DateTimeField, \
    EmbeddedDocumentListField

from src.utils import str_object_id


class SlackFormField(EmbeddedDocument):
    id = StringField(required=True, default=str_object_id)
    type = StringField()
    title = StringField()
    options = ListField(StringField())
    meta = dict(strict=False)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "options": self.options,
        }


class SlackForm(Document):
    team_id = StringField()
    user_id = StringField()
    user_name = StringField()
    name = StringField()
    fields = EmbeddedDocumentListField(SlackFormField)
    meta = dict(strict=False)

    def number_of_submissions(self):
        return Submission.objects.filter(form_id=str(self.pk)).count()


    def to_dict(self):
        return {
            "id": str(self.pk),
            "team_id": self.team_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "name": self.name,
            "fields": [field.to_dict() for field in self.fields],
            "number_of_submissions": self.number_of_submissions(),
        }


class SubmissionField(EmbeddedDocument):
    title = StringField()
    value = StringField()

    @property
    def display_title(self):
        if not self.title.endswith('?') and not self.title.endswith(':'):
            return self.title + ':'
        return self.title


class Submission(Document):
    form_id = StringField()
    user_id = StringField()
    user_name = StringField()
    fields = ListField(EmbeddedDocumentField(SubmissionField))
    created_at = DateTimeField(default=datetime.datetime.now)

    @property
    def formatted_date(self):
        return self.created_at.strftime('%b. %-d, %Y')

    @property
    def formatted_time(self):
        return self.created_at.strftime('%H:%M')

    def to_dict(self):
        return {
            "id": str(self.pk),
            "form_id": self.form_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "fields": [field.to_dict() for field in self.fields],
            "created_at": self.created_at.isoformat(),
            "formatted_date": self.formatted_date,
            "formatted_time": self.formatted_time,
        }