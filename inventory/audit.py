from inventory.models import AuditLog
from django.contrib.auth.models import User

def log_action(user, action, model_name, object_id, details=""):
    """
    Helper function to create audit log entries
    """
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id),
        details=details
    )