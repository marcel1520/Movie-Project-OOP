from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp

storage_options = input("Please choose between storage option (1) for 'json' or (2) for 'csv': ")

def main():
    while True:
        if storage_options == "1":
            storage1 = StorageJson("film_database.json")
            movie_app1 = MovieApp(storage1)
            movie_app1.run()
            storage1.create_html()
        if storage_options == "2":
            storage = StorageCsv("film_database.csv")
            storage.save_movie()
            movie_app = MovieApp(storage)
            movie_app.run()
        elif storage_options != "1" or storage_options != "2":
            break
            # csv storage is not yet activated

if __name__ == "__main__":
    main()
