from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from atlas.apps.account.models import User
from atlas.apps.account.serializers import ContactSerializer

class ContactListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAdminUser,)
