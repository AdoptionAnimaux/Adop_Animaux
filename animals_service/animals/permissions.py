from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Lecture : tout utilisateur authentifié
    Écriture : permission admin
    """

    def has_permission(self, request, view):
        # Lecture (GET)
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Écriture (POST, PUT, DELETE)
        return request.user.has_perm("animals.can_publish_animal")
