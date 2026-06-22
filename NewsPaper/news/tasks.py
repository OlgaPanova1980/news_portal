from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body=preview,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def weekly_send_email():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body="Привет! Новые статьи за неделю в твоем любимом разделе!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()