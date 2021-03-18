import pathlib # модуль упрощает работу с файлами и папками
import shutil # модуль, позволяющий копировать, перемещать и удалять файлы и папки


class Pathfinder:  # Патфайндер хранит информацию о путях
    
    def __init__(self, sep : str) -> None:
        self.sep = sep
        self.__depot = ["depot"]

    # функция добавляет файл в общую иерархию
    def add_path(self, path: str) -> None:

        # перейти на уровень вверх
        if ".." in path and len(self.__depot) != 1:
            self.__depot.pop(-1)

        # выйти за пределы иерархии
        elif ".." in path:
            print("Ошибка: выход за пределы иерархии")

        else:
            self.__depot.append(path)

    @property
    def path(self):
        # current path
        absol = pathlib.Path(__file__).parent.absolute()
        return str(absol) + self.sep + self.sep.join(self.__depot)

    @property
    def upper_path(self):
        # upper path
        absol = pathlib.Path(__file__).parent.absolute()
        print(self.__depot[1:])
        return str(absol) + self.sep + self.sep.join(self.__depot[:1])

    def filebynamepath(self, file_name: str) -> str:
        # возвращает нужный нам файл в сохранённом пути иерархии
        locdepot = self.__depot.copy()
        locdepot.append(file_name)
        # назначаем абсолютный путь
        absol = pathlib.Path(__file__).parent.absolute()
        return str(absol) + self.sep + self.sep.join(locdepot)