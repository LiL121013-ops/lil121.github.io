from django.shortcuts import render, redirect
from photo.models import Photo
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from .models import UserProfile
import oss2

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from .models import Photo

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Image
import requests


@login_required
def add_images(request):
    # 获取随机图片
    response = requests.get('https://api.example.com/random_images')
    images = response.json()

    # 将图片保存到数据库
    for image in images:
        Image.objects.create(url=image['url'], user=request.user)

    return render(request, 'your_template.html')

def logout_view(request):
    # 删除用户的图片
    Image.objects.filter(user=request.user).delete()

    # 注销用户
    logout(request)

    return redirect('login_page')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('photo_album')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    else:
        return render(request, 'login.html')
@login_required
def photo_album(request):
    # 获取所有照片
    photos = Photo.objects.filter(user=request.user)
    return render(request, 'photo_album.html', {'photos': photos})

def delete_photo(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        photo.delete()
    return redirect('photo_gallery')

class ObjIterator(oss2.ObjectIteratorV2):
    # 初始化时立即抓取图片数据
    def __init__(self, bucket):
        super().__init__(bucket)
        self.fetch_with_retry()

    # 分页要求实现__len__
    def __len__(self):
        return len(self.entries)

    # 分页要求实现__getitem__
    def __getitem__(self, key):
        return self.entries[key]

    # 修改图片排序方式
    def _fetch(self):
        result = self.bucket.list_objects_v2(prefix=self.prefix,
                                          delimiter=self.delimiter,
                                          continuation_token=self.next_marker,
                                          start_after=self.start_after,
                                          fetch_owner=self.fetch_owner,
                                          encoding_type=self.encoding_type,
                                          max_keys=self.max_keys,
                                          headers=self.headers)
        self.entries = result.object_list + [oss2.models.SimplifiedObjectInfo(prefix, None, None, None, None, None)
                                             for prefix in result.prefix_list]
        # 让图片以上传时间倒序
        self.entries.sort(key=lambda obj: -obj.last_modified)

        return result.is_truncated, result.next_continuation_token

def oss_home(request):
    raise ValueError("""
请确保 /photo/views.py 中有关阿里云的信息填写正确。
(即 auth 和 bucket 属性中的信息)。
完成后将它们取消注释，并删除此行raise代码。""")

    photos       = ObjIterator(bucket)
    paginator    = Paginator(photos, 6)
    page_number  = request.GET.get('page')
    paged_photos = paginator.get_page(page_number)
    context      = {'photos': paged_photos}


    # 省略登入登出的POST请求代码
    # ...

    return render(request, 'photo/oss_list.html', context)



def home(request):
    photos = Photo.objects.all()
    paginator    = Paginator(photos, 5)
    page_number  = request.GET.get('page')
    paged_photos = paginator.get_page(page_number)
    context = {'photos': paged_photos}

    # 处理登入登出的POST请求
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(request, username=username, password=password)
        # 登入
        if user is not None and user.is_superuser:
            login(request, user)
        # 登出
        isLogout  = request.POST.get('isLogout')
        if isLogout == 'True':
            logout(request)
    return render(request, 'photo/list.html', context)


def upload(request):
    if request.method == 'POST' and request.user.is_superuser:
        images = request.FILES.getlist('images')
        for i in images:
            photo = Photo(image=i)
            photo.save()
    return redirect('home')





from django.http import JsonResponse

# 无限滚动
def fetch_photos(request):
    photos       = Photo.objects.values()
    paginator    = Paginator(photos, 4)
    page_number  = int(request.GET.get('page'))
    data         = {}

    # 页码正确才返回数据
    if page_number <= paginator.num_pages:
        paged_photos = paginator.get_page(page_number)
        data.update({'photos': list(paged_photos)})

    return JsonResponse(data)