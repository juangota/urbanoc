# coding=utf8
'import pdb; pdb.set_trace()'

from rest_framework.permissions import IsAdminUser

from rest_framework import serializers

from django.contrib.auth.models import User

from urbanocapp.models import Author, UrbanOcurrence, OcurrenceLocation

class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer of the User model used in UserViewSet
    '''
    class Meta:
        model = User
        fields = ('id',
                  'url',
                  'username',
                  'email')


class AuthorSerializer(serializers.ModelSerializer):
    '''
    Serializer of the Author model used in AuthorViewSet

    Validators in the name field had to be removed to solve 
    the issue of DRF with updates and creates of related fields
    with unique constrains.
    '''
    class Meta:
        model = Author
        fields = ('id',
                  'name',
                  'phone',
                  'email')
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }


class OcurrenceLocationSerializer(serializers.ModelSerializer):
    '''
    Serializer of the UcurrenceLocation model used in OcurrenceLocationViewSet

    Validators in the "name" field had to be removed to solve 
    the issue of DRF with updates and creates of related fields
    with unique constrains.
    '''
    class Meta:
        model = OcurrenceLocation
        fields = ('id',
                  'name',
                  'longitude',
                  'latitude')
        extra_kwargs = {
            'name': {'validators': []},
        }


class UrbanOcurrenceUserSerializer(serializers.ModelSerializer):
    '''
    Serializer of the UcurrenceLocation model used in OcurrenceLocationViewSet

    It was asked that, in the creation of an Urba Ocurrence, also the author 
    and location shoukd be created. Thus, the create and update method of the 
    serializer had to be ovewriten in order to create the related objects 
    Author and Location.

    As only admin user can update the "status" field, another serializer 
    exists, equals t this one, but with the addition of that field, named 
    UrbanOcurrenceAdminSerializer.
    '''
    aut = AuthorSerializer(source='author')
    local = OcurrenceLocationSerializer(source='location')
    class Meta:
        model = UrbanOcurrence
        fields = ('id',
                  'description',
                  'category',
                  'aut',
                  'local')

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_name = author_data.pop('name')

        location_data = validated_data.pop('location')
        location_name = location_data.pop('name')

        author, created = Author.objects.update_or_create(name=author_name,
                                                  defaults={**author_data})
        location, created = OcurrenceLocation.objects \
                                             .update_or_create(
                                                  name=location_name,
                                                  defaults={**location_data})
        urbanoc = UrbanOcurrence.objects.create(author=author,
                                                location=location,
                                                **validated_data)

        return urbanoc

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author_name = author_data.pop('name')

        location_data = validated_data.pop('location')
        location_name = location_data.pop('name')

        author, created = Author.objects.update_or_create(name=author_name,
                                                  defaults={**author_data})
        location, created = OcurrenceLocation.objects \
                                             .update_or_create(
                                                  name=location_name,
                                                  defaults={**location_data})
        instance.author = author
        instance.location = location
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()

        return instance


class UrbanOcurrenceAdminSerializer(serializers.ModelSerializer):
    '''
    Serializer of the UcurrenceLocation model used in OcurrenceLocationViewSet

    It was asked that, in the creation of an Urba Ocurrence, also the author 
    and location shoukd be created. Thus, the create and update method of the 
    serializer had to be ovewriten in order to create the related objects 
    Author and Location.

    As only admin user can update the "status" field, another serializer 
    exists, equals this one, but without that field, named 
    UrbanOcurrenceUserSerializer.
    '''
    aut = AuthorSerializer(source='author')
    local = OcurrenceLocationSerializer(source='location')
    class Meta:
        model = UrbanOcurrence
        fields = ('id',
                  'description',
                  'status',
                  'category',
                  'aut',
                  'local')

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author_name = author_data.pop('name')

        location_data = validated_data.pop('location')
        location_name = location_data.pop('name')

        author, created = Author.objects.update_or_create(name=author_name,
                                                  defaults={**author_data})
        location, created = OcurrenceLocation.objects \
                                             .update_or_create(
                                                  name=location_name,
                                                  defaults={**location_data})
        urbanoc = UrbanOcurrence.objects.create(author=author,
                                                location=location,
                                                **validated_data)

        return urbanoc

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author_name = author_data.pop('name')

        location_data = validated_data.pop('location')
        location_name = location_data.pop('name')

        author, created = Author.objects.update_or_create(name=author_name,
                                                  defaults={**author_data})
        location, created = OcurrenceLocation.objects \
                                             .update_or_create(
                                                  name=location_name,
                                                  defaults={**location_data})
        instance.author = author
        instance.location = location
        instance.status = validated_data.get('status', instance.status)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()

        return instance

# class UrbanOcurrenceUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UrbanOcurrence
#         fields = ('id',
#                   'description',
#                   'category',
#                   'author',
#                   'location')


# class UrbanOcurrenceAdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UrbanOcurrence
#         fields = ('id',
#                   'description',
#                   'status',
#                   'category',
#                   'author',
#                   'location')
