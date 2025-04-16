class MovieApp:
    def __init__(self, storage):
        self._storage = storage
        self._commands = {
            "0": self._command_exit_movie_app,
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_movie_random,
            "7": self._command_movie_search,
            "8": self._command_movie_sort_rating,
            "9": self._command_movie_sort_year,
            "10": self._command_add_new_field, # use for json version
            "11": self._generate_website
        }

    @staticmethod
    def _command_exit_movie_app():
        print("Exiting movie app")
        exit()

    def _command_list_movies(self):
        print("\n******* LIST OF MOVIES *******\n")
        print(self._storage.list_movies())


    def _command_add_movie(self):
        self._storage.add_movie("Enter title: ")

    def _command_delete_movie(self):
        self._storage.delete_movie("Enter title to delete: ")

    def _command_update_movie(self):
        self._storage.update_movie("Enter title to update: ", "Enter new rating: ")

    def _command_movie_stats(self):
        print(self._storage.stats_movie())

    def _command_movie_random(self):
        print(self._storage.random_movie())

    def _command_movie_search(self):
        print(self._storage.search_movie())

    def _command_movie_sort_rating(self):
        print(self._storage.rating_sorted_movie())

    def _command_movie_sort_year(self):
        print(self._storage.year_sorted_movie())

    def _command_add_new_field(self):
        self._storage.add_field_to_movies("runtime", "update movie to add runtime") # use for json version

    def _generate_website(self):
        print("\nGenerating Website...")
        self._storage.create_html()

    def run(self):
        while True:
            print("\n******* Movie Database *******")
            print("\nMovie Database Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Sort movie by ratings")
            print("9. Sort movie by year")
            print("10. Add new field to database")
            print("11. Generate website")

            choice = input("Enter an option (0-11): ").strip()
            command = self._commands.get(choice)

            if command:
                command()
            else:
                print("Enter valid choice.")


