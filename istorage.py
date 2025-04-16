from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def fetch_movie_data(self, title):
        pass

    @abstractmethod
    def load_movies(self):
        pass

    @abstractmethod
    def add_field_to_movies(self, field_name, default_value):
        pass

    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def save_movie(self):
        pass

    @abstractmethod
    def add_movie(self, title):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        pass

    @abstractmethod
    def stats_movie(self):
        pass

    @abstractmethod
    def random_movie(self):
        pass

    @abstractmethod
    def search_movie(self):
        pass

    @abstractmethod
    def rating_sorted_movie(self):
        pass

    @abstractmethod
    def year_sorted_movie(self):
        pass

    @abstractmethod
    def create_html(self):
        pass

