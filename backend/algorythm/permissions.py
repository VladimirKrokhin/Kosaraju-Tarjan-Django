from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее только владельцам объектов редактировать их.
    """


    def has_object_permission(self, request, view, obj):
        # Чтение разрешена любому запросу,
        # следовательно разрешены GET, HEAD или 
        # OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Разрешение на запись разрешены только владельцам
        return obj.owner == request.user

    
class IsGraphOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.graph.owner == request.user

