# Generated by Django 5.0.2 on 2024-02-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0003_remove_replycomment_reply_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(default='', upload_to='media/post/images/'),
        ),
    ]
