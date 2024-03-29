import datetime
import logging
from enum import Enum
from typing import List

import pytz as pytz
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, EmbeddedDocument, \
    EmbeddedDocumentField, IntField

from src.slack_api.slack_user import SlackUser
from src.utils import DAYS_OF_THE_WEEK


class ScheduledTimeStatus(Enum):
    Pending = 'Pending'
    Success = 'Success'
    Failed = 'Failed'


class TimeField(EmbeddedDocument):
    hour = IntField()
    minute = IntField()
    meta = dict(strict=False)

    def __str__(self):
        return f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}"


class FormSchedule(Document):
    user_id = StringField()
    user_name = StringField()
    form_id = StringField()
    days_of_the_week = ListField(IntField())
    send_to = StringField()  # channel or 'me'
    timezone = StringField()
    time_local = EmbeddedDocumentField(TimeField)
    meta = dict(strict=False)

    def save_and_schedule_next(self) -> "ScheduledEvent":
        self.save()
        try:
            next_event = self.schedule_next()
        except Exception as e:
            logging.exception("Failed to schedule next. Deleting schedule")
            self.delete()
            raise e
        return next_event

    def schedule_next(self) -> "ScheduledEvent":
        execution_time_utc = self.get_next_time()
        next_event = ScheduledEvent(
            schedule=self,
            execution_time_utc=execution_time_utc,
            status=ScheduledTimeStatus.Pending.value
        )
        next_event.save()
        return next_event

    def get_next_time(self) -> datetime.datetime:
        """ Returns the next time when this schedule should happen """
        tz = pytz.timezone(self.timezone)
        now_local = datetime.datetime.now(datetime.timezone.utc).astimezone(tz)
        target_time_local = now_local.replace(hour=self.time_local.hour,
                                              minute=self.time_local.minute,
                                              second=0,
                                              microsecond=0)
        if target_time_local <= now_local:
            target_time_local += datetime.timedelta(days=1)

        while target_time_local.weekday() not in self.days_of_the_week:
            target_time_local += datetime.timedelta(days=1)
        return target_time_local.astimezone(datetime.timezone.utc)

    def get_next_times(self, days) -> List[datetime.datetime]:
        """ Returns the next times when this schedule should happen, in the next [days] number of days """
        times = []
        tz = pytz.timezone(self.timezone)
        now_local = datetime.datetime.now(datetime.timezone.utc).astimezone(tz)
        end_date = now_local + datetime.timedelta(days=days)
        target_time_local = now_local.replace(hour=self.time_local.hour,
                                              minute=self.time_local.minute,
                                              second=0,
                                              microsecond=0)
        if target_time_local <= now_local:
            target_time_local += datetime.timedelta(days=1)

        while target_time_local < end_date:
            if target_time_local.weekday() in self.days_of_the_week:
                times.append(target_time_local.astimezone(datetime.timezone.utc))
            target_time_local += datetime.timedelta(days=1)
        return times

    def get_events_to_schedule(self, days) -> List["ScheduledEvent"]:
        """ Returns this schedule's events, in the next [days] number of days """
        events = []
        for execution_time_utc in self.get_next_times(days):
            existing = ScheduledEvent.objects(schedule=self, execution_time_utc=execution_time_utc).first()
            if not existing:
                next_event = ScheduledEvent(
                    schedule=self,
                    execution_time_utc=execution_time_utc,
                    status=ScheduledTimeStatus.Pending.value
                )
                events.append(next_event)
            elif not existing.slack_message_id:
                events.append(existing)
        return events

    def schedule_description(self) -> str:
        weekdays = ', '.join([DAYS_OF_THE_WEEK[weekday] for weekday in self.days_of_the_week])
        return f"{weekdays} at {str(self.time_local.hour).zfill(2)}:{str(self.time_local.minute).zfill(2)} ({self.timezone})"


    def send_to_name(self) -> str:
        """ Where this scheduled form will be sent. Either a slack channel, or a username """
        if self.send_to.startswith('#'):
            return self.send_to
        return '@' + SlackUser(self.send_to).username


class ScheduledEvent(Document):
    schedule = ReferenceField(FormSchedule)
    execution_time_utc = DateTimeField()
    status = StringField()
    slack_message_id = StringField()
    meta = dict(strict=False)
