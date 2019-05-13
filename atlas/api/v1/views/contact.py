import operator
import functools
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from django.db.models import Q

from atlas.apps.contact.models import Contact
from atlas.apps.contact.serializers import ContactSerializer


class ContactListView(ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        contact_query = self.request.query_params.get("query")
        contact_category = self.request.query_params.getlist("category")

        queryset = Contact.objects.all()
        if contact_category:
            user_pref = {}
            for category in contact_category:
                user_pref[category] = True
            queryset = queryset.filter(preference__contains=user_pref)

        if contact_query:
            queries = contact_query.split()
            search_args = []
            for q in queries:
                for f in ('first_name__icontains', 'last_name__icontains', 'email__icontains'):
                    search_args.append(Q(**{f: q}))
            queryset = queryset.filter(functools.reduce(operator.or_, search_args))

        return queryset.order_by('first_name', 'last_name')
