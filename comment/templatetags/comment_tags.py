from django import template

# Create your tags here.
register = template.Library()

@register.inclusion_tag('comment/comment.html')
def load_comment(article, user):
    return {
        'article': article,
        'user': user,
    }
