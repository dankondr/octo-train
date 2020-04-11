from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def new_user(self, **kwargs):
        """Function to create new user row from kwargs."""
        pass

    @abstractmethod
    def solved_today(self, problem_type):
        """Function that retrieves number of problems with type == problem_type which solved today."""
        pass

    @abstractmethod
    def get_solved(self, problem_type):
        """Function that retrieves set of solved problems with type == problem_type"""
        pass

    @abstractmethod
    def get_not_solved(self, problem_type):
        """Function that retrieves set of not solved problems with type == problem_type"""
        pass

    @abstractmethod
    def get_all(self, problem_type):
        """Function that retrieves set with all of the problems with type == problem_type"""
        pass

    @abstractmethod
    def get_not_solved_problem(self, problem_type):
        """Function that retrieves random not solved problem with type == problem_type"""
        pass

    @abstractmethod
    def insert(self, problem_data):
        """Function that inserts provided problem data in database."""
        pass

    @abstractmethod
    def update_user(self, key, value):
        """Function that updates users row."""
        pass
