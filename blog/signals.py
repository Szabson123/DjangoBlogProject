from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from blog.models import Subscribe

@receiver(post_save, sender=Post)
def send_post_update_email(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscribe.objects.all()
        for subscriber in subscribers:
            send_mail('Nowy Post na blogu', f'Hej na blogu został zapostwoany nowy post o tytule: "{instance.title}"',
                      settings.EMAIL_HOST_USER,
                      [subscriber.email],
                      fail_silently=False,
                      )
