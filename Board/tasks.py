from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(**kwargs):

    send_mail(
        subject='Ваш комментарий принят',
        message=f'Автор публикации {kwargs["board_author"]} принял ваш комментарий "{kwargs["comment_text"]}"',
        from_email='Samurraich@yandex.kz',
        recipient_list=[kwargs['user_email']],
    )


@shared_task
def send_email_new_comment(**kwargs):

    send_mail(
        subject='Уведомление о новом комментарии',
        message=f'У вашей публикации "{kwargs["board_title"]}" новый комментарий: {kwargs["comment_text"]}.\n'
                f'Автор комментария: {kwargs["comment_author"]}',
        from_email='Samurraich@yandex.kz',
        recipient_list=[kwargs["email"]],
    )
