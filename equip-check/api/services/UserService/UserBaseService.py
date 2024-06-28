from abc import ABC, abstractmethod


class UserBaseService(ABC):

    @abstractmethod
    def login(self):
        """ Abstarct method for User Log in """
        pass

    @abstractmethod
    def logout(self):
        """ Abstarct method for User Log out """
        pass
