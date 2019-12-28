import markdown
from markdown.extensions.toc import TocExtension

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db.models.aggregates import Count

from ..models import Category, Tag 

# Create your tags here.
register = template.Library()

@register.inclusion_tag('blog/article_info.html')
def load_article_info(article, is_index):    
    return {
        'article': article,
        'is_index': is_index,
    }


@register.filter(is_safe=True)
@stringfilter
def markdown_content(content):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    md_content = md.convert(content)
    md_content = md_content.replace('<table>', '<table class="table table-bordered">')
    return mark_safe(md_content)


@register.filter(is_safe=True)
@stringfilter
def markdown_toc(content):
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    md.convert(content)
    md_toc = md.toc
    return mark_safe(md_toc)


@register.inclusion_tag('blog/pagination.html')
def load_pagination(paginator, page_obj, is_paginated, is_search, query):
    if not is_paginated:    
        return {
            'is_paginated': is_paginated,
        }
    left = []
    right = []
    left_has_more = False
    right_has_more = False
    first = False
    last = False
    page_number = page_obj.number
    total_pages = paginator.num_pages
    page_range = paginator.page_range
    if page_number == 1:
        right = page_range[page_number:page_number + 2]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True
    elif page_number == total_pages:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    else:
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    if left_has_more:
        left_more = page_number - 3
    else:
        left_more = 1
    if right_has_more:
        right_more = page_number + 3
    else:
        right_more = total_pages
    if not is_search:
        page_href = '?page'
    else:
        page_href = '?q={}&page'.format(query)
    return {
        'is_paginated': is_paginated,
        'page_href': page_href,
        'page_obj': page_obj,
        'paginator': paginator,
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
        'left_more': left_more,
        'right_more': right_more,
    }


@register.inclusion_tag('blog/category_tag_list.html')
def load_category():
    category_list = Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0).order_by('-num_articles')
    return {
        'object_list': category_list,
    }


@register.inclusion_tag('blog/category_tag_list.html')
def load_tag():
    tag_list = Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0).order_by('-num_articles')
    return {
        'object_list': tag_list,
    }
