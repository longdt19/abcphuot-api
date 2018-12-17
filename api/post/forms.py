from api.common.base_forms import ValidationError, BaseCreateForm, BaseListForm, BaseReadForm, BaseUpdateForm, IdField, \
    fields, STRING_LENGTH_VALIDATORS, BaseForm

from .constants import POST_CATEGORIES

# class CreateBlogForm(BaseCreateForm):
#     title = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
#     category_id = PostCategoryField(required=True)
#     content = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['EX_LONG'])
#
# class UpdateBlogForm(BaseUpdateForm):
#     title = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
#     content = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_LARGE'])
#     category_id = PostCategoryField()








class PostCategoryField(fields.Field):
    def _validate(self, value):
        if value not in list(map(lambda item: item['id'], POST_BLOG_CAT)):
            raise ValidationError('Invalid category_id!')


class PostCategoryField(fields.Field):
    def _validate(self, value):
        if value not in list(map(lambda item: item['id'], POST_CATEGORIES)):
            raise ValidationError('Invalid category_id!')


class CreateBannerForm(BaseCreateForm):
    name = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    object_id = IdField()
    object_type = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_SHORT'])


class UpdateBannerForm(BaseUpdateForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    object_id = IdField()
    object_type = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_SHORT'])


class GetBannerForm(BaseForm):
    id = IdField()
    slug = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])


class ListBannerForm(BaseListForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])


class CreatePostForm(BaseCreateForm):
    name = fields.String(required=True, validate=STRING_LENGTH_VALIDATORS['LONG'])
    category_id = PostCategoryField(required=True)
    banner = IdField()


class UpdatePostForm(BaseUpdateForm):
    name = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
    content = fields.String(validate=STRING_LENGTH_VALIDATORS['EX_LARGE'])
    category_id = PostCategoryField()


class GetPostForm(BaseForm):
    id = IdField()
    slug = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])


class ListPostForm(BaseListForm):
    categories = fields.List(PostCategoryField())
    search_text = fields.String(validate=STRING_LENGTH_VALIDATORS['LONG'])
