from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    while True:
        storage_options = input("Please choose between storage option (1) for 'json' or (2) for 'csv': ")
        if storage_options == "1":
            storage1 = StorageJson("film_database.json")
            movie_app1 = MovieApp(storage1)
            movie_app1.run()
            storage1.create_html()
        if storage_options == "2":
            try:
                storage = StorageCsv("film_database.csv")
                storage.save_movie()
                movie_app = MovieApp(storage)
                movie_app.run()
            except TypeError:
                print("csv storage not active. Press (0) to exit.")
                continue
        elif storage_options != "1" or storage_options != "2":
            break
            # csv storage is not yet activated

if __name__ == "__main__":
    main()
