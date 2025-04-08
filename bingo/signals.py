import os
import shutil
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings


@receiver(post_migrate)
def create_special_users(sender, **kwargs):
    """
    Creates special users (gamekeeper and developer) after migrations are completed.
    """
    if sender.name != 'bingo':
        return

    User = apps.get_model('bingo', 'User')

    GAMEKEEPER_PASSWORD = "MYPASS123"
    DEVELOPER_PASSWORD = "MYDEV123"

    if not User.objects.filter(username='GAMEKEEPER').exists():
        gamekeeper = User.objects.create_user(
            username='GAMEKEEPER',
            email='mk811@exeter.ac.uk',
            password=GAMEKEEPER_PASSWORD
        )
        gamekeeper.role = 'GameKeeper'
        gamekeeper.is_staff = True
        gamekeeper.save()
        print("✅ Created gamekeeper user")

    if not User.objects.filter(username='DEVELOPER').exists():
        developer = User.objects.create_user(
            username='DEVELOPER',
            email='myosandarkyaw22@gmail.com',
            password=DEVELOPER_PASSWORD
        )
        developer.role = 'Developer'
        developer.is_staff = True
        developer.is_superuser = True
        developer.save()
        print("✅ Created developer user")


@receiver(post_save, sender=apps.get_model('bingo', 'Profile'))
def copy_profile_picture_to_static(sender, instance, **kwargs):
    """
    After a profile is saved, copy its profile picture to the static directory
    for serving in production.
    """
    if instance.profile_picture:
        try:
            src_path = instance.profile_picture.path
            dest_dir = os.path.join(settings.BASE_DIR, 'static', 'profile_pics')
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, os.path.basename(src_path))
            shutil.copy(src_path, dest_path)
            print(f"📸 Copied profile picture to: {dest_path}")
        except Exception as e:
            print(f"⚠️ Error copying profile picture: {e}")
