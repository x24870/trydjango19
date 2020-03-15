from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'
    # my_safe_method = ['PUT', 'GET']
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        # Or you can check if the user is active
        # user = User.objects.get(user=request.user)
        # if not user.is_active: return False
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user