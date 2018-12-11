from api.common.base_forms import ValidationError, BaseCreateForm, BaseListForm, BaseReadForm, BaseUpdateForm, IdField, \
    fields, STRING_LENGTH_VALIDATORS, BaseForm


class BaseStorageForm(BaseForm):
    # object_id = IdField(required=True)
    # object_type = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['EX_SHORT'])
    pass


class CreateImageForm(BaseStorageForm, BaseCreateForm):
    pass


class ListImageForm(BaseStorageForm, BaseListForm):
    pass


class DownloadFileForm(BaseForm):
    path = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
