# coding=utf8
'import pdb; pdb.set_trace()'

# Create your views here.

from django.contrib.auth.models import User

from django.contrib.gis.measure import D 
from django.contrib.gis.geos import fromstr

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from urbanocapp.models import Author, UrbanOcurrence, OcurrenceLocation
# from urbanocapp.permissions import IsOwnerOrAdminOrReadOnly
from urbanocapp.serializers import UserSerializer, \
                                   AuthorSerializer, \
                                   UrbanOcurrenceUserSerializer, \
                                   UrbanOcurrenceAdminSerializer, \
                                   OcurrenceLocationSerializer


class UserViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.

    Only admins can see registered app users.

    To manage users, the admmin can use the django 
    user administration default (ex: http://127.0.0.1:8000/admin)
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AuthorViewSet(ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.

    Only authenticated users may edit authors.

    Admin users can edit any author. Regular user only can edit 
    authors introduces by themselfs.
    """
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OcurrenceLocationViewSet(ModelViewSet):
    """
    API endpoint that allows ocurrences locations to be viewed or edited.

    Only authenticated users may edit ocurrence locations.
    """
    queryset = OcurrenceLocation.objects.all()
    serializer_class = OcurrenceLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UrbanOcurrenceViewSet(ModelViewSet):
    """
    API endpoint that allows urban ocurrences to be viewed or edited.

    Only authenticated users may edit ocurrence locations.

    To access an ocurrence add the ocurrence id to the urban_ocurrences 
    url (ex: http://127.0.0.1:8000/urban_ocurrences/1)

    To filter by author add "?author=<author_id>"  to the urban_ocurrences 
    url (ex: http://127.0.0.1:8000/urban_ocurrences/?author=1)

    To filter by category add "?category=<category_string>"  to the urban_ocurrences 
    url (ex: http://127.0.0.1:8000/urban_ocurrences/?category=special_event). 
    "category_string" must be one of [construction, special_event, incident, 
                                      weather_condition, road_condition]

    To filter by location, the user must provide ref_lat, ref_lon and radius of search 
    (ocurrences closer than radius from ref point), 
    optionally the user may provide the units of radius (by default, units are m).
    Ex: http://127.0.0.1:8000/urban_ocurrences/?ref_lat=40.0&ref_lon=-8.0&radius=50&rad_units=km
    """
    queryset = UrbanOcurrence.objects.none()
    permission_classes = [IsAuthenticatedOrReadOnly]#,
                          #IsOwnerOrAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UrbanOcurrenceAdminSerializer
        return UrbanOcurrenceUserSerializer

    def get_queryset(self):
        ref_lat = self.request.GET.get('ref_lat', None)
        ref_lon = self.request.GET.get('ref_lon', None)
        radius = self.request.GET.get('radius', None)
        radius_units = self.request.GET.get('rad_units', 'm')

        author = self.request.GET.get('author', None)

        category = self.request.GET.get('category', None)

        queryset = UrbanOcurrence.objects.all()

        if ref_lat and ref_lon and radius:    
            ref_pnt = fromstr("POINT(%s %s)" % (ref_lon, ref_lat))
            distance_from_point = {radius_units:radius}

            queryset = queryset.filter(location__point__distance_lte=(ref_pnt,
                                                    D(**distance_from_point) ))

        if author:
            queryset = queryset.filter(author_id=author)

        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)
