import re
from marshmallow import fields, ValidationError, Schema
from bson import ObjectId
from datetime import datetime

from .constants import PAGINATION, STRING_LENGTH

STRING_LENGTH_VALIDATORS = {
    'EX_SHORT': lambda value: len(value) <= STRING_LENGTH['EX_SHORT'],
    'SHORT': lambda value: len(value) <= STRING_LENGTH['SHORT'],
    'MEDIUM': lambda value: len(value) <= STRING_LENGTH['MEDIUM'],
    'LONG': lambda value: len(value) <= STRING_LENGTH['LONG'],
    'EX_LONG': lambda value: len(value) <= STRING_LENGTH['EX_LONG'],
    'LARGE': lambda value: len(value) <= STRING_LENGTH['LARGE'],
    'EX_LARGE': lambda value: len(value) <= STRING_LENGTH['EX_LARGE']
}

PHONE_REGEX = r'^[0-9\-\+]{9,15}$'


class IdField(fields.Field):
    def _serialize(self, value, attr, obj):
        return ObjectId(value)

    def _validate(self, value):
        if isinstance(value, ObjectId):
            return value
        try:
            ObjectId(value)
        except Exception as error:
            raise ValidationError('Invalid Id %s' % error.args)


class PhoneField(fields.Field):
    def _validate(self, value):
        if not value:
            return
        if not isinstance(value, str) or not re.compile(PHONE_REGEX).match(value):
            raise ValidationError('Invalid phone.')


class EmailField(fields.Email):
    def _validate(self, value):
        if not value:
            return
        super()._validate(value=value)


class DatetimeField(fields.Field):
    def _validate(self, value):
        try:
            value = float(value)
            datetime.fromtimestamp(value)
        except (ValueError, TypeError):
            raise ValidationError('Invalid datetime!')

    def _serialize(self, value, attr, obj):
        return float(value)


class BaseForm(Schema):
    pass


class BaseCreateForm(BaseForm):
    pass


class BaseUpdateForm(BaseForm):
    id = IdField(required=True)


class BaseReadForm(BaseForm):
    id = IdField(required=True)


class BaseListForm(BaseForm):
    page = fields.Integer(default=PAGINATION['page'])
    per_page = fields.Integer(default=PAGINATION['per_page'])
    order = fields.String(default='-created_at', validate=STRING_LENGTH_VALIDATORS['MEDIUM'])


class BaseDeleteForm(BaseForm):
    id = IdField(required=True)
