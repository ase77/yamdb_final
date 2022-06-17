from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class_list = (User, Category, Genre, Title, GenreTitle, Review, Comment)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for value in class_list:
            if value.objects.exists():
                print(f'''{value.__name__} data already loaded
                {ALREDY_LOADED_ERROR_MESSAGE}
                ''')
            else:
                print(f'Loading {value.__name__} data')

        for row in DictReader(
                open('./static/data/users.csv', encoding="utf8")):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()

        for row in DictReader(
                open('./static/data/category.csv', encoding="utf8")):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        for row in DictReader(
                open('./static/data/genre.csv', encoding="utf8")):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        for row in DictReader(
                open('./static/data/titles.csv', encoding="utf8")):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category']
            )
            title.save()

        for row in DictReader(
                open('./static/data/genre_title.csv', encoding="utf8")):
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id']
            )
            genre_title.save()

        for row in DictReader(
                open('./static/data/review.csv', encoding="utf8")):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()

        for row in DictReader(
                open('./static/data/comments.csv', encoding="utf8")):
            comment = Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date']
            )
            comment.save()
