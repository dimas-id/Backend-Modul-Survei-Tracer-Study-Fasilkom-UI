from atlas.common.permissions import IsOwnerOfObject


class IsOwnerOfExperience(IsOwnerOfObject):

    def get_user_field(self):
        return 'owner'