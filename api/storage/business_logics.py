import os
from flask import g, send_file

from config import Config

from api.common.base_errors import InvalidRequestParams
from api.common.base_logics import BaseLogic
from api.product.models import Product, Category
from api.post.models import Banner, Post

from .errors import *
from .models import Image
from .uploaders import uploader
from .constants import VALID_IMAGE_EXTS

OBJECT_TYPE_MAP = {
    'product': Product,
    'product-category': Category,
    'banner': Banner,
    'post': Post
}


class StorageBL(BaseLogic):
    def _make_url(self, file_path):
        return Config.DOMAIN + '/download?params={"path":"%s"}' % file_path

    def _is_file_ext_valid(self, filename, valid_exts):
        split_name = filename.split('.')
        file_ext = split_name[len(split_name) - 1]
        return file_ext in valid_exts

    def download(self, path):
        if not os.path.exists(path):
            raise InvalidRequestParams('File not found!', payload=path)

        return send_file(path, as_attachment=True)


class ImageBL(StorageBL):
    def create(self, object_id, object_type, file):
        if not self._is_file_ext_valid(filename=file.filename, valid_exts=VALID_IMAGE_EXTS):
            raise InvalidFileExt('Invalid image ext!')

        obj = self._get_object(object_id=object_id, object_type=object_type, type_map=OBJECT_TYPE_MAP)

        image = Image()

        path, size = uploader.upload(file=file)

        image.url = self._make_url(file_path=path)

        image.name = file.name
        image.path = path
        image.size = size
        image.object_type = object_type
        image.content_type = file.content_type
        image.object_id = object_id
        image.created_by = g.user.id

        image.create()

        obj.patch(update_params=dict(push__images=image.id))
        return image.output()

    def delete(self, id):
        image = self._get_record_by_id(model=Image, id=id)
        obj = self._get_object(object_id=image.object_id, object_type=image.object_type, type_map=OBJECT_TYPE_MAP)

        uploader.remove(image.path)
        image.delete()
        obj.patch(update_params=dict(pull__images=image.id))
        return dict(success=True)

    def list(self, object_id, object_type, page, per_page, order):
        params = dict(object_type=object_type, object_id=object_id)
        matches = Image.objects(**params).order_by(order)
        total = matches.count(True)
        result = [image.output() for image in matches.paginate(page=page, per_page=per_page).items]
        return dict(total=total, result=result)


image_bl = ImageBL()
storage_bl = StorageBL()
