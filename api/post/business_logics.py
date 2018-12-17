from slugify import slugify
from flask import g
from mongoengine import Q

from api.common.base_logics import BaseLogic
from api.common.base_errors import InvalidRequestParams, PermissionError
from api.storage.models import Image
from api.storage.uploaders import uploader

from .models import Banner, Post
from .errors import *

OBJECT_TYPE_MAP = {
    'home-page': None
}


class PostBlogBL(BaseLogic):
    def create(self, title, category_id, banner_id, content=None):
        post = Post()
        post.name = name
        post.category_id = category_id
        post.content = content
        post.banner = banner_id
        post.create()
        post.save()
        return post.output()

    def update(self, id, title, category_id, content=None):
        post = self._get_record_by_id(model=Post, id=id)
        update_params = dict()
        if content is not None:
            update_params['content'] = content

        if title:
            update_params['title'] = title

        if category_id:
            update_params['category_id'] = category_id

        if update_params:
            update_params['updated_by'] = g.user.id
            post.patch(update_params=update_params)
        return dict(success=True)

        def list(self, page, per_page, order, search_text=None, categories=None):
            params = dict()
            if categories:
                params['category_id__in'] = categories

            if search_text:
                params['slug__contains'] = slugify(search_text)

            matches = Post.objects(**params).order_by(order)

            total = matches.count(True)
            result = []
            for post in matches.paginate(page=page, per_page=per_page).items:
                post_output = post.output()
                for index, image_id in enumerate(post.images):
                    image = Image.objects(id=image_id).first()
                    post_output['images'][index] = image.url
                result.append(post_output)
            return dict(total=total, result=result)

        def get_one(self, id=None, slug=None):
            if not id and not slug:
                raise InvalidRequestParams('Must pass atleast id or slug!')

            if id:
                post = self._get_record_by_id(model=Post, id=id)

            else:
                post = Post.objects(slug=slug).first()

            if not post:
                return dict()

            result = post.output()
            for index, image_id in enumerate(post.images):
                image = Image.objects(id=image_id).first()
                result['images'][index] = image.url

            return result

        def delete(self, id):
            post = self._get_record_by_id(id=id, model=Post)
            images = Image.objects(object_id=post.id, object_type='post')
            for image in images:
                uploader.remove(image.path)
            images.delete()
            post.delete()
            return dict(success=True)

class BannerBL(BaseLogic):
    def _is_name_duplicate(self, name, id=None):
        params = dict(slug=slugify(name))
        if id:
            params['id__ne'] = id
        return Banner.objects(**params).first() is not None

    def create(self, name, object_type=None):
        if self._is_name_duplicate(name=name):
            raise NameAlreadyExists

        banner = Banner()
        banner.name = name

        if object_type:
            if object_type not in OBJECT_TYPE_MAP.keys():
                raise InvalidRequestParams('Invalid banner object_type!')

            banner.object_type = object_type

        banner.create()
        return banner.output()

    def update(self, id, name=None, object_type=None):
        banner = self._get_record_by_id(id=id, model=Banner)
        update_params = dict()

        if name:
            if self._is_name_duplicate(name=name, id=id):
                raise NameAlreadyExists
            update_params['name'] = name

        if object_type:
            if object_type not in OBJECT_TYPE_MAP.keys():
                raise InvalidRequestParams('Invalid banner object_type!')

            update_params['object_type'] = object_type

        if update_params:
            update_params['updated_by'] = g.user.id
            banner.patch(update_params=update_params)

        return dict(success=True)

    def delete(self, id):
        banner = self._get_record_by_id(id=id, model=Banner)
        for image_id in banner.images:
            image = Image.objects(id=image_id).first()
            image.delete()
        banner.delete()
        return dict(success=True)

    def get(self, id=None):
        if id:
            banner = self._get_record_by_id(model=Banner, id=id)
        else:
            banner = Banner.objects(is_default=True).first()
            if not banner:
                banner = Banner.objects.first()

        if not banner:
            return dict()

        return banner.output()

    def list(self, page, per_page, order, name=None):
        params = dict()
        if name:
            params['slug__contains'] = slugify(name)
        matches = Banner.objects(**params).order_by(order)
        total = matches.count(True)
        result = []
        for banner in matches.paginate(page=page, per_page=per_page).items:
            banner_output = banner.output()
            for index, image_id in enumerate(banner.images):
                image = Image.objects(id=image_id).first()
                banner_output['images'][index] = image.url
            result.append(banner_output)
        return dict(result=result, total=total)


class PostBL(BaseLogic):
    def create(self, name, category_id, banner):
        post = Post()
        post.name = name
        post.category_id = category_id
        post.banner = banner
        post.create()

        post_output = post.output()
        if banner:
            image = Image.objects(id=banner).first()
            post_output['image'] = image.url
        return post_output

    def update(self, id, content=None, name=None, category_id=None):
        post = self._get_record_by_id(model=Post, id=id)
        update_params = dict()
        if content is not None:
            update_params['content'] = content

        if name:
            update_params['name'] = name

        if category_id:
            update_params['category_id'] = category_id

        if update_params:
            post.patch(update_params=update_params)
        return dict(success=True)

    def list(self, page, per_page, order, search_text=None, categories=None):
        params = dict()
        if categories:
            params['category_id__in'] = categories

        if search_text:
            params['slug__contains'] = slugify(search_text)

        matches = Post.objects(**params).order_by(order)

        total = matches.count(True)
        result = []
        for post in matches.paginate(page=page, per_page=per_page).items:
            post_output = post.output()

            image_id = post.banner
            if image_id:
                image = Image.objects(id=image_id).first()
                post_output['banner_url'] = image.url

            result.append(post_output)
        return dict(total=total, result=result)

    def get_one(self, id=None, slug=None):
        if not id and not slug:
            raise InvalidRequestParams('Must pass atleast id or slug!')

        if id:
            post = self._get_record_by_id(model=Post, id=id)

        else:
            post = Post.objects(slug=slug).first()

        if not post:
            return dict()

        result = post.output()
        for index, image_id in enumerate(post.images):
            image = Image.objects(id=image_id).first()
            result['images'][index] = image.url

        return result

    def delete(self, id):
        post = self._get_record_by_id(id=id, model=Post)
        post.delete()
        return dict(success=True)


banner_bl = BannerBL()
post_bl = PostBL()
postblog_bl = PostBlogBL()
