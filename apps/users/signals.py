from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, app_config=None, **kwargs):
    """
    Create default user groups after database migration.
    
    This signal handler creates the following groups if they don't exist:
    - Admin: For administrative users (superusers)
    - Staff: For staff members
    
    Args:
        sender: The app config that triggered the migration.
        app_config: The AppConfig instance.
        **kwargs: Additional keyword arguments.
    """
    if app_config.name != "apps.users":
        return

    # Define default groups
    groups_data = {
        "Admin": {
            "description": "Administrative users with full system access",
        },
        "Staff": {
            "description": "Staff members with limited system access",
        },
    }

    for group_name, group_info in groups_data.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Created group: {group_name}")
        else:
            print(f"Group already exists: {group_name}")


__all__ = ["create_default_groups"]
