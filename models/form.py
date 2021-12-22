from mongoengine import Document, StringField, EmbeddedDocument, ListField, EmbeddedDocumentField, BooleanField


class SlackFormField(EmbeddedDocument):
    type = StringField()
    title = StringField()


class SlackForm(Document):
    user_id = StringField()
    user_name = StringField()
    form_name = StringField()
    fields = ListField(EmbeddedDocumentField(SlackFormField))
    public = BooleanField()
