from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Post, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.postCategory.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            for sub in subscribers:
                if sub.email and sub.email not in subscribers_emails:
                    subscribers_emails.append(sub.email)

        if subscribers_emails:
            subject = f'Новая статья в любимом разделе: {instance.title}'

            text_content = (
                f'Здравствуйте! Новая статья на портале: {instance.title}\n\n'
                f'Краткое содержание: {instance.text[:50]}...\n'
                f'Ссылка на статью: http://127.0.0{instance.id}'
            )

            html_content = (
                f'<p>Здравствуйте! Новая статья в твоём любимом разделе!</p>'
                f'<h2>{instance.title}</h2>'
                f'<p>{instance.text[:50]}...</p>'
                f'<a href="http://127.0.0{instance.id}">Читать статью целиком</a>'
            )

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subscribers_emails,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()