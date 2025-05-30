from rest_framework.permissions import BasePermission, SAFE_METHODS
from donations.models import Donations


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission for project operations:

    - Safe methods (GET, HEAD, OPTIONS): allowed for any authenticated user.
    - POST (create): only allowed for users with type 'admin' or 'owner'.
    - DELETE: allowed only for the project owner or admin, and only if 
      total donations are less than 25% of the project's target amount.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        if request.method == 'POST':
            return (
                request.user.is_authenticated and
                request.user.type in ('owner', 'admin')
            )

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        is_owner = obj.user_id == request.user
        is_admin = request.user.type == 'admin'

        if not (is_owner or is_admin):
            return False

        # Restrict DELETE if donations ≥ 25% of target
        if request.method == 'DELETE':
            donations = Donations.objects.filter(project=obj)
            total_donated = sum(d.amount for d in donations)

            try:
                target = float(obj.target)
            except (TypeError, ValueError):
                return False

            if total_donated >= 0.25 * target:
                return False

        return True
