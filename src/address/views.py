from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.serializers import AddressSerializers


class AddressList(generics.ListCreateAPIView):
    """Create or list a users addresses.

    User must be authenticated.  Can only list Addresses the user has created.
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializers

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get Update or Delete a users own address.

    User must be authenticated.
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializers

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
