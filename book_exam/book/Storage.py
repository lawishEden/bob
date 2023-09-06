from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        # 重新上传文件
        import os, time, hashlib
        # 获取文件后缀
        ext = os.path.splitext(name)[1]

        # 文件目录
        d = os.path.dirname(name)

        # 定义文件夹名称
        fn = hashlib.md5(time.strftime('%Y%m%d%H%M%S').encode('utf-8')).hexdigest()
        name = os.path.join(d, fn + ext)

        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)
