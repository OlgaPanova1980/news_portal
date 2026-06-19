import datetime
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category

logger = logging.getLogger(__name__)


def weekly_digest_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)

    if not posts.exists():
        return

    categories = Category.objects.all()
    for category in categories:
        category_posts = posts.filter(postCategory=category)

        if category_posts.exists():
            subscribers = category.subscribers.all()
            subscribers_emails = [sub.email for sub in subscribers if sub.email]

            if subscribers_emails:
                subject = f'Еженедельный дайджест новых статей в категории {category.name}'

                links_html = ""
                links_text = ""
                for post in category_posts:
                    links_html += f'<li><a href="http://127.0.0{post.id}">{post.title}</a></li>'
                    links_text += f'- {post.title}: http://127.0.0{post.id}\n'

                text_content = f'Привет! Вот новые статьи за неделю в разделе {category.name}:\n\n{links_text}'
                html_content = f'<p>Привет! Вот новые статьи за неделю в разделе <b>{category.name}</b>:</p><ul>{links_html}</ul>'

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers_emails,
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_digest_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="weekly_digest_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_digest_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

