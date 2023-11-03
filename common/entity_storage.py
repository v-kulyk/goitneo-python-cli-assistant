from collections import UserDict
from typing import Type
import pickle

class EntityStorage:
    def __init__(self, entity_name:str, entity_class:Type[UserDict], demo_filler:callable=None) -> None:
        self.entity_name = entity_name
        self.entity_class = entity_class

        self.demo_filler = demo_filler

    def load(self) -> UserDict:
        try:
            with open(self.__get_path(), 'rb') as fh:
                data = pickle.load(fh)

                if isinstance(data, self.entity_class):
                    return data
        except FileNotFoundError:
            pass

        entity = self.entity_class()

        if self.demo_filler and len(entity) == 0:
            self.demo_filler(entity)

        return entity

    def save(self, entity:UserDict):
        with open(self.__get_path(), 'wb') as fh:
            pickle.dump(entity, fh)

    def __get_path(self):
        return self.entity_name + "_demo.dat" if self.demo_filler else self.entity_name + ".dat"