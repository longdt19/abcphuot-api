from slugify import slugify

from api.product.models import Category as ProductCategory, Product
from api.user.models import User, Role
from api.user.methods import encrypt

from .data import roles, users, product_categories


class Seed(object):
    def role(self):
        Role.drop_collection()

        for role_data in roles:
            name = role_data['name']

            role = Role()
            role.name = name
            role.slug = slugify(name)
            role.is_default = True
            role.create()

    def user(self):
        User.drop_collection()
        for user_data in users:
            name = user_data['name']
            email = user_data['email']
            password = user_data['password']
            role = Role.objects(slug=user_data['role']).first()

            user = User()
            user.name = name
            user.slug = slugify(name)
            user.email = email
            user.password = encrypt(password)
            user.role_id = role.id
            user.create()

    def product_category(self):
        ProductCategory.drop_collection()

        for category_data in product_categories:
            name = category_data['name']

            parent = ProductCategory()
            parent.name = name
            parent.slug = slugify(name)
            parent.create()

            children = category_data['children']
            for child_data in children:
                name = child_data['name']
                child = ProductCategory()
                child.parent_id = parent.id
                child.slug = slugify(name)
                child.name = name
                child.create()

    def reset_db(self):
        Product.drop_collection()
        self.role()
        self.user()
        self.product_category()
