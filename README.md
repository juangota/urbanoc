# urbanoc
API to manage urban ocurrences

Install:
1. pip install -r requirements.txt
2. Create a postgres database and user with postgis extension (refer to: https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/postgis/)
3. update NAME, USER and PASSWORD in the DATABASES section of urbanoc/settings.py, according to the settings defined in 2.
4. Migrations: python manage.py makemigrations; python manage.py migrate
5. Create a user to interact with the api: python manage.py createsuperuser
6. run development server: python manage.py runserver
7. List or Create urban ocurrences: http://localhost:8000/urban_ocurrences/ (as well as author and associated location)
9. Filter urban ocurrences by author: http://localhost:8000/urban_ocurrences/?author=<author_id>
10. Filter urban ocurrences by category: http://localhost:8000/urban_ocurrences/?category=<category_string>.
	"category_string" must be one of [construction, special_event, incident, weather_condition, road_condition]
11. To filter by location, the user must provide ref_lat, ref_lon and radius of search 
    (ocurrences closer than radius from ref point), 
    optionally the user may provide the units of radius (by default, units are m).
    Ex: http://localhost:8000/urban_ocurrences/?ref_lat=40.0&ref_lon=-8.0&radius=50&rad_units=km