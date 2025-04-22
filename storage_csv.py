from istorage import IStorage
import csv
import random
import statistics
import requests
from dotenv import load_dotenv
import os
from requests.exceptions import ConnectionError, Timeout, RequestException


class StorageCsv(IStorage):
    # load_dotenv(".env")
    api_key = "12433447" # os.getenv("API_KEY")
    base_url = url = f"http://www.omdbapi.com/?apikey={api_key}"

    def __init__(self, file_path="film_database.csv"):
        self.file_path = file_path
        self.movies = self.load_movies()

    def make_url(self, title):
        return f"{self.base_url}&t={title}"

    def fetch_movie_data(self, title):
        url = self.make_url(title)
        try:
            req = requests.get(url, timeout=5)
            movie_data = req.json()
            if movie_data["Response"] == "False":
                print("No movie found with that name.")
            return movie_data
        except ConnectionError:
            print("unable to connect to the internet")
        except Timeout:
            print("The request timed out, please try again later")
        except RequestException as e:
            print(f"an unexpected error occurred {e}")

    def load_movies(self):
        movies = {}
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row["title"]
                movies[title] = {
                    "title": title,
                    "director": row.get("director", "update for director"),
                    "release_year": int(row["release_year"]),
                    "rating": float(row["rating"]),
                    "genre": row.get("genre", "update for genre"),
                    "poster": row.get("poster", "update for poster")
                }
        return movies

    def add_field_to_movies(self, field_name, default_value):
        self.movies = self.load_movies()
        for movie in self.movies.values():
            movie[field_name] = default_value
        self.save_movie()

    def list_movies(self):
        self.movies = self.load_movies()
        print(f"{len(self.movies)} Movies in the database\n")
        all_films = ""
        for movie_info in self.movies.values():
            all_films += (f"{movie_info['title']} -- "
                          f"director: {movie_info['director']} -- "
                          f"release year: {movie_info['release_year']} -- "
                          f"rating: {movie_info['rating']} -- "
                          f"genre: {movie_info['genre']} -- "
                          f"poster: {movie_info['poster']}\n")
        return all_films

    def save_movie(self):
        fieldnames = ["title", "director", "release_year", "rating", "genre", "poster"]
        with open("film_database.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for movie in self.movies.values():
                writer.writerow({
                    "title": movie["title"],
                    "director": movie["director"],
                    "release_year": movie["release_year"],
                    "rating": movie["rating"],
                    "genre": movie["genre"],
                    "poster": movie["poster"]
                })

    def add_movie(self, title):
        title = input(title).strip()
        movie_info = self.fetch_movie_data(title)
        try:
            director = movie_info["Director"]
            year = int(movie_info["Released"][-4:])
            rating = float(movie_info["Ratings"][0]["Value"][0:3])
            genre = movie_info["Genre"]
            poster = movie_info["Poster"]
            self.movies[title] = {
                'title': title,
                'director': director,
                'release_year': year,
                'rating': rating,
                'genre': genre,
                'poster': poster
            }
            self.save_movie()
            print("movie added successfully")
            return self.movies
        except TypeError:
            print("please check internet connection")
        except KeyError:
            print("Title not available in API")

    def delete_movie(self, title):
        delete_title = input(title).strip()
        if delete_title in self.movies:
            self.movies.pop(delete_title)
            self.save_movie()
            print(f"'{delete_title}' deleted successfully.")
        else:
            print(f"'{delete_title}' not found in database.")

    def update_movie(self, title, rating):
        update_title = input(title).strip()
        movie_info = self.fetch_movie_data(update_title)
        if update_title in self.movies:
            try:
                update_director = movie_info["Director"]
                update_genre = movie_info["Genre"]
                update_poster = movie_info["Poster"]
                current_year = self.movies[update_title]["release_year"]
                rating = self.movies[update_title]["rating"]
                self.movies[update_title] = {
                    'title': update_title,
                    'director': update_director,
                    'release_year': current_year,
                    'rating': rating,
                    'genre': update_genre,
                    'poster': update_poster
                }
                self.save_movie()
                print(f"{update_title} has been updated.")
            except TypeError:
                print("please check internet connection")
        else:
            print(f"Movie {update_title} not found in database")


    def stats_movie(self):
        if len(self.movies) == 0:
            print_info = "\nNo movies in database\n"
            return print_info
        else:
            def get_average():
                val_list = []
                average_rating = 0
                for val in self.movies.values():
                    rating = val["rating"]
                    val_list.append(rating)
                    average_rating = statistics.mean(val_list)
                print_average = f"\nThe average rating is: {average_rating:.2f}"
                return print_average

            average_get = get_average()

            def get_median():
                val_list = []
                for val in self.movies.values():
                    rating = val["rating"]
                    val_list.append(rating)
                    val_list.sort()
                val_list = val_list[::-1]
                median = len(val_list) // 2
                if len(val_list) % 2 != 0:
                    print_med = f"The median value is: {val_list[median]}"
                    return print_med, val_list
                else:
                    median = len(val_list) // 2
                    print_med = f"The median value is: {(val_list[median - 1] + val_list[median]) / 2}"
                    return print_med, val_list

            med_value, values_list = get_median()

            def get_best_worst_ratings(list_of_vals):
                highest_rating = max(list_of_vals)
                lowest_rating = min(list_of_vals)
                best_list = []
                worst_list = []
                for value in self.movies.values():
                    title = value["title"]
                    rating = value["rating"]
                    if rating == highest_rating:
                        best_list.append(title)
                        best_list.append(rating)
                    if rating == lowest_rating:
                        worst_list.append(title)
                        worst_list.append(rating)
                print_info_best = f"Highest Rating {best_list[1]}: movie(s) -> {', '.join(best_list[::2])}"
                print_info_worst = f"Lowest Rating {worst_list[1]}: movie(s) -> {', '.join(worst_list[::2])}\n"
                return print_info_best, print_info_worst

            get_best_movie, get_worst_movie = get_best_worst_ratings(values_list)
            print_info = f"{average_get}\n{med_value}\n{get_best_movie}\n{get_worst_movie}"
            return print_info

    def random_movie(self):
        random_item = random.choices(list(self.movies.values()))
        display_random_choice = f"Random Choice: {random_item[0]["title"]} from {random_item[0]["release_year"]} rated {random_item[0]["rating"]}."
        return display_random_choice

    def search_movie(self):
        dict_lower_keys = {key.lower(): value for key, value in self.movies.items()}
        user_input_search_movie = input("\nEnter part of movie name: ").lower()
        print_info = ""
        for movie, movie_info in dict_lower_keys.items():
            if user_input_search_movie in movie:
                print_info += f"\n{movie.title()}: {movie_info["release_year"]} {movie_info["rating"]}"
        return print_info

    def rating_sorted_movie(self):
        self.movies = self.load_movies()

        def get_ratings_list(ratings_dict):
            ratings_list = []
            for key, val in ratings_dict.items():
                ratings_list.append((key, val["rating"]))
            return ratings_list

        def get_rating(tuple_rating):
            return tuple_rating[1]

        def sort_database_rating(tup_list):
            sorted_films_database = {}
            for movie, rating in tup_list:
                sorted_films_database.update({
                    movie: {
                        "title": movie,
                        "release_year": self.movies[movie]["release_year"],
                        "rating": rating
                    }
                })
            return sorted_films_database

        def display_dict_rating(ratings_sorted_films):
            return_info = ""
            for details in ratings_sorted_films.values():
                return_info += f"{details['title']}: -- release year: {details['release_year']} -- rating: {details['rating']}\n"
            return return_info

        ratings_list_get = get_ratings_list(self.movies)
        sorted_by_rating = sorted(ratings_list_get, key=get_rating, reverse=True)
        database_rating_sort = sort_database_rating(sorted_by_rating)
        return display_dict_rating(database_rating_sort)

    def year_sorted_movie(self):
        self.movies = self.load_movies()

        def get_years_list(dict_films):
            year_list = []
            for key, val in dict_films.items():
                year_list.append((val["title"], val["release_year"]))
            return year_list

        def get_year(y_tuple):
            return y_tuple[1]

        def sort_database_year(tuple_list):
            sorted_films_database = {}
            for movie, year in tuple_list:
                sorted_films_database.update({movie: {
                    "title": movie,
                    "release_year": year,
                    "rating": self.movies[movie]["rating"]
                }})
            return sorted_films_database

        def display_dict_year(years_dict):
            return_info = ""
            for details in years_dict.values():
                return_info += f"{details['title']}: -- release year: {details['release_year']} -- rating: {details['rating']}\n"
            return return_info

        year_tuple = get_years_list(self.movies)
        sorted_year = sorted(year_tuple, key=get_year)
        dict_year_create = sort_database_year(sorted_year)
        return display_dict_year(dict_year_create)

    def create_html(self):
        def serialize_movie_info(title):
            movie_info = self.fetch_movie_data(title)
            title = movie_info["Title"]
            year = movie_info["Released"][-4:]
            rating = movie_info["Ratings"][0]["Value"][0:3]
            genre = movie_info["Genre"]
            poster = movie_info["Poster"]
            runtime = movie_info["Runtime"]

            return f"""
                <li>
                  <div class='movie'>
                    <img src="{poster}" alt="{title} poster" />
                    <h2>{title}</h2>
                    <p><strong>Genre:</strong> {genre}</p>
                    <p><strong>Year:</strong> {year}</p>
                    <p><strong>Runtime:</strong> {runtime}</p>
                    <p><strong>Rating:</strong> {rating}</p>
                  </div>
                </li>
                """


        def get_movies():
            self.movies = self.load_movies()
            return "".join(serialize_movie_info(title) for title in self.movies)

        def read_html_file():
            with open("_static/index_template.html", "r") as html_movie_file:
                return html_movie_file.read()

        def replace_movie_grid(template_html, movie_html):
            return template_html.replace("__TEMPLATE_MOVIE_GRID__", movie_html)

        def write_movie_html(movie_html_replaced):
            movie_html = "_static/index.html"
            with open(movie_html, "w") as new_movie_file:
                new_movie_file.write(movie_html_replaced)
            print("HTML page successfully created!")

        template = read_html_file()
        movie_grid = get_movies()
        final_html = replace_movie_grid(template, movie_grid)
        write_movie_html(final_html)



