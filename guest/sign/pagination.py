from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 分页


def paginator(data, page):
    paginator = Paginator(data, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)  # page不是整数，取第一页
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)  # page不在范围，取最后一页
    return contacts
