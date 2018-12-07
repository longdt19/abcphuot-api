from api.common.base_forms import ValidationError, BaseCreateForm, BaseListForm, BaseReadForm, BaseUpdateForm, IdField, \
    fields, STRING_LENGTH_VALIDATORS, BaseForm


class AuthForm(BaseForm):
    email = fields.Email(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    password = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
