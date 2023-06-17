from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Comment, Board
from .tasks import send_email_new_comment


@receiver(post_save, sender=Comment)
def send_message(sender, instance, created, **kwargs):
    if created:
        id = instance.board_id
        board = Board.objects.get(id=id)
        email = board.author.email
        comment_author = User.objects.get(id=instance.author_id)

        send_mail(
            subject='Уведомление о новом комментарии',
            message=f'У вашей публикации "{board.title}" новый комментарий: {instance.text}.\n'
                    f'Автор комментария: {comment_author}',
            from_email='Samurraich@yandex.kz',
            recipient_list=[email],
        )

