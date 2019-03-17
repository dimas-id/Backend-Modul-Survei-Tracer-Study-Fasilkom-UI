from rest_framework.permissions import (
    IsAuthenticated, BasePermission, SAFE_METHODS)


class IsOwnerOfObject(BasePermission):

    # override this, some model has different user field
    user_field = 'user'
    user_identifier = 'pk'

    def get_user_field(self):
        """
        Return the string of user_field.
        You can override this or the field.
        This method intended for inherintence.
        """
        return self.user_field

    def get_user_identifier(self):
        """
        Return the string of user_identifier.
        user_identifier is user identifier in REST URI
        Example:
        ```
        path('/users/<user_id>/balls/<pk>)
        ```
        the <user_id> is the variable that we use to identify the ownership.
        so set 'user_id' as user_identifier

        You can override this or the field.
        This method intended for inherintence.
        """
        return self.user_identifier

    def is_user_identifier_valid(self, request, view):
        return str(getattr(request.user, 'pk')) == view.kwargs[self.get_user_identifier()]

    def has_object_permission(self, request, view, obj):
        """
        Check object level permission.
        Check if the object is owned by authenticated user.
        """
        user_of_the_object = getattr(obj, self.get_user_field(), None)
        # if user None, just return False
        # and let the view handle the rest
        return user_of_the_object is not None \
            and user_of_the_object.id == request.user.id

    def has_permission(self, request, view):
        """
        Must be authenticated
        """
        return super().has_permission(request, view) \
            and IsAuthenticated().has_permission(request, view) \
            and self.is_user_identifier_valid(request, view)


class IsOwnerOfObjectOrReadOnly(IsOwnerOfObject):

    def has_object_permission(self, request, view, obj):
        """
        If safe method, grant the permission to view. Others is restricted.
        """
        has_perm = super().has_object_permission(request, view, obj)
        return request.method in SAFE_METHODS or has_perm

    def is_user_identifier_valid(self, request, view):
        return request.method in SAFE_METHODS \
            or super().is_user_identifier_valid(request, view)
