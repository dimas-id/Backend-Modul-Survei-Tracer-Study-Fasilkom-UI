from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from atlas.apps.contact.models import Contact
from atlas.apps.contact.serializers import ContactSerializer

class ContactListView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAdminUser,)
