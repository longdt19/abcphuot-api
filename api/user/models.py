from api.common.base_models import BaseDocument, db, STRING_LENGTH, Person


class Role(BaseDocument):
    name = db.StringField(max_length=STRING_LENGTH['LONG'], required=True)


class User(Person, BaseDocument):
    password = db.StringField(required=True, max_length=STRING_LENGTH['EX_LONG'])

    role_id = db.ObjectIdField(required=True)

    def output(self, result=None, includes=None, excludes=None):
        if not excludes:
            excludes = ['password']
        else:
            excludes.append('password')

        return super().output(result=result, includes=includes, excludes=excludes)
