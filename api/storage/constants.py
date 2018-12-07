import os

from api.common.constants import APP_ROOT_DIR

UPLOAD_DIR = os.path.join(APP_ROOT_DIR, 'static/upload')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

VALID_IMAGE_EXTS = ['jpg', 'png']
