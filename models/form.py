import datetime

from mongoengine import Document, StringField, EmbeddedDocument, ListField, EmbeddedDocumentField, BooleanField, \
    DateTimeField, EmbeddedDocumentListField

from util.utils import str_object_id


class SlackFormField(EmbeddedDocument):
    id = StringField(required=True, default=str_object_id)
    type = StringField()
    title = StringField()
    meta = dict(strict=False)


class SlackForm(Document):
    user_id = StringField()
    user_name = StringField()
    name = StringField()
    fields = EmbeddedDocumentListField(SlackFormField)
    public = BooleanField()
    meta = dict(strict=False)


class SlackFormSubmissionField(EmbeddedDocument):
    title = StringField()
    value = StringField()


class SlackFormSubmission(Document):
    form_id = StringField()
    user_id = StringField()
    fields = ListField(EmbeddedDocumentField(SlackFormSubmissionField))
    created_at = DateTimeField(default=datetime.datetime.now)
