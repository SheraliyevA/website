# Generated by Django 5.0.2 on 2024-02-17 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_comments_replycomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replycomment',
            name='reply_comment',
        ),
        migrations.RemoveField(
            model_name='replycomment',
            name='replier_name',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='ReplyComment',
        ),
    ]
