from django.db import migrations

def create_admin_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    admin_group, created = Group.objects.get_or_create(name='Admin')

    user_permissions = Permission.objects.filter(
        content_type__app_label='auth', 
        codename__in=['add_user', 'change_user', 'delete_user', 'view_user']
    )
    blog_permissions = Permission.objects.filter(
        content_type__app_label='blog', 
        codename__in=['add_blog', 'change_blog', 'delete_blog', 'view_blog']
    )

    admin_group.permissions.add(*user_permissions)
    admin_group.permissions.add(*blog_permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_admin_group),
    ]

