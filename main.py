from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp

def main():
    """storage = StorageCsv("film_database.csv")
    storage.save_movie()
    movie_app = MovieApp(storage)
    movie_app.run()"""
    storage1 = StorageJson("film_database.json")
    movie_app1 = MovieApp(storage1)
    movie_app1.run()
    storage1.create_html()
    # storage1.add_field_to_movies("runtime", "update movie to add runtime")

if __name__ == "__main__":
    main()
