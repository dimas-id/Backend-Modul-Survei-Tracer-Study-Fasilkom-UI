from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from django.db.models import Q

from atlas.apps.contact.models import Contact
from atlas.apps.contact.serializers import ContactSerializer

class ContactListView(ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        contact_name = self.request.query_params.get("name")
        contact_category = self.request.query_params.getlist("category")
        
        queryset = Contact.objects.all()
        if contact_category is not None:
            user_pref = {}
            for category in contact_category:
                user_pref[category] = True
            queryset = queryset.filter(preference__contains=user_pref)

        if contact_name is not None:
            queryset = queryset.filter(Q(first_name__icontains=contact_name) | Q(last_name__icontains=contact_name))

        return queryset
