# -*- coding: utf-8 -*-

import math

from bson import ObjectId
from slugify import slugify
from flask_mongoengine import BaseQuerySet
from mongoengine.queryset import QuerySet
from .constants import STRING_LENGTH
from .methods import get_now
from .constants import DATE_FORMAT

from api.extensions import db


class Serializer(object):
    def parse_value(self, field, value, *args, **kwargs):
        if value is None:
            return value

        if isinstance(field, db.DateTimeField):
            return value.strftime(DATE_FORMAT)

        if isinstance(field, db.ReferenceField):
            return str(value.id)

        if isinstance(field, db.ObjectIdField):
            return str(value)

        if isinstance(field, db.EmbeddedDocumentField):
            return value.output()

        if isinstance(field, db.ListField) or isinstance(field, db.EmbeddedDocumentListField):
            result = []
            # element's field type of the list
            element_field = field.field
            if element_field:
                for val in value:
                    result.append(self.parse_value(element_field, val, *args, **kwargs))
            else:
                result = value
            return result

        return value

    def output(self, result=None, includes=None, excludes=None):
        if not result or not isinstance(result, dict):
            result = dict()

        all_fields = self._fields

        if not includes or not isinstance(includes, list):
            includes = []

        if not excludes or not isinstance(excludes, list):
            excludes = []

        result_fields = dict()

        if includes:
            for field_name, field in all_fields.items():
                if field_name in includes:
                    result_fields[field_name] = field
        else:
            for field_name, field in all_fields.items():
                if field_name not in excludes:
                    result_fields[field_name] = field

        for field_name, field in result_fields.items():
            result[field_name] = self.parse_value(
                field=field, value=getattr(self, field_name))

        return result


class FieldChecker(object):
    def get_required_fields(self):
        required_fields = []
        for field_name, field in self._fields.items():
            if not field_name.startswith('_') and field.required:
                required_fields.append(field_name)
        return required_fields

    def check_required_fields(self):
        required_fields = self.get_required_fields()
        missing = []
        data = self._data
        # check required fields
        for field_name in required_fields:
            if field_name not in data.keys() or data.get(field_name) is None:
                missing.append(field_name)
        if missing:
            raise Exception('Missing required fields %s' % missing)


class Pagination(object):

    def __init__(self, iterable, page, per_page):

        if page < 1:
            page = 1

        self.iterable = iterable
        self.page = page
        self.per_page = per_page

        if isinstance(iterable, QuerySet):
            self.total = iterable.count()
        else:
            self.total = len(iterable)

        start_index = (page - 1) * per_page
        end_index = page * per_page

        self.items = iterable[start_index:end_index]
        if isinstance(self.items, QuerySet):
            self.items = self.items.select_related()

    @property
    def pages(self):
        """The total number of pages"""
        return int(math.ceil(self.total / float(self.per_page)))

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.iterable is not None, ('an object is required '
                                           'for this method to work')
        iterable = self.iterable
        if isinstance(iterable, QuerySet):
            iterable._skip = None
            iterable._limit = None
        return self.__class__(iterable, self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert self.iterable is not None, ('an object is required '
                                           'for this method to work')
        iterable = self.iterable
        if isinstance(iterable, QuerySet):
            iterable._skip = None
            iterable._limit = None
        return self.__class__(iterable, self.page + 1, self.per_page)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                    num > self.pages - right_edge or
                    (num >= self.page - left_current and num <= self.page + right_current)):
                if last + 1 != num:
                    yield None
                yield num
                last = num
        if last != self.pages:
            yield None


class Base(object):
    slug = db.StringField()
    created_at = db.FloatField(default=get_now)
    updated_at = db.FloatField()

    created_by = db.ObjectIdField()
    updated_by = db.ObjectIdField()

    deleted = db.BooleanField(default=False)
    is_default = db.BooleanField(default=False)


class NewQuerySet(BaseQuerySet):
    def paginate(self, page, per_page, **kwargs):
        """
        Paginate the QuerySet with a certain number of docs per page
        and return docs for a given page.
        """
        return Pagination(self, page, per_page)


class BaseDocument(db.Document, Base, Serializer):
    meta = {
        'allow_inheritance': True,
        'abstract': True,
        'queryset_class': NewQuerySet
    }

    def create(self):
        if hasattr(self, 'name') and hasattr(self, 'slug') and self.name:
            self.slug = slugify(self.name)
        return self.save()

    def patch(self, update_params=None):
        if update_params:
            name = update_params.get('name')
            if hasattr(self, 'name') and hasattr(self, 'slug') and name:
                update_params['slug'] = slugify(name)
            update_params['updated_at'] = get_now()
            self.update(**update_params)
            return self.reload()

        self.updated_at = get_now()
        if hasattr(self, 'name') and hasattr(self, 'slug') and self.name:
            self.slug = slugify(self.name)
        return self.save()

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<%s - item: %r>' % (self._meta['collection'], self.name)
        return '<%s: %r>' % (self._meta['collection'], self.id)


class BaseEmbeddedDocument(db.EmbeddedDocument, Base, Serializer, FieldChecker):
    meta = {
        'allow_inheritance': True
    }
    id = db.ObjectIdField(default=lambda: ObjectId())


class SimpleEmbeddedDocument(db.EmbeddedDocument, Serializer, FieldChecker):
    meta = {
        'allow_inheritance': True
    }


class Person(object):
    email = db.StringField(max_length=STRING_LENGTH['LONG'])
    phone = db.StringField(max_length=STRING_LENGTH['EX_SHORT'])
    name = db.StringField(max_length=STRING_LENGTH['MEDIUM'])
    address = db.StringField(max_length=STRING_LENGTH['LONG'])
    gender = db.StringField(default='unknown')
    birthday = db.DictField()
