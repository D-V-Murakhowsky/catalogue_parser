from .core import Singleton
import pathlib

class GoogleConnector(metaclass=Singleton):

    def __init__(self):
        self.client


    def _get_credentials_path(self):
        path = pathlib.Path(__file__).parents[1].resolve() / 'assets/client_secret.json'