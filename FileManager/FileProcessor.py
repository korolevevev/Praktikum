# В данном классе собраны функции, обеспечивающие работу с файлами

from typing import Dict
import os

from Pathfinder import Pathfinder
import shutil # модуль, позволяющий копировать, перемещать и удалять файлы и папки

class FileProcessor:
    @staticmethod
    def get_cmds() -> Dict[str, str]:

        cmds = {
            "cd": "change dir",
            "ls": "dir contains",
            "mkdir": "make dir",
            "rmdir": "remove dir",
            "touch": "new file",
            "rename": "rename file dir",
            "read": "read file",
            "remove": "remove file",
            "copy": "cope file dir",
            "move": "move file dir",
            "write": "write into file",
        }

        return cmds

    def __init__(self) -> None:
        self.sep = os.sep
        self.depot = Pathfinder(self.sep)

    # имена функций соответствуют именам команд из словаря 'cmds' (описание функционала каждой функции соответствует значению по ключу в том же словаре)
    
    def cd(self, name: str):
        
        # можем перемещаться в текущей папке, открывать любую по её названиб и переходить вверх по иерархии
        
        self.depot.add_path(name)
        this_path = self.depot.path

        try: os.chdir(this_path)
        except FileNotFoundError: 
            self.depot.add_path(f"..{self.sep}")
            print(f"Ошибка: директории {name} не существует")
        except NotADirectoryError: 
            self.depot.add_path(f"..{self.sep}")
            print(f"Ошибка: файл {name} не является директорией")

    def mkdir(self, name: str):

        this_path = self.depot.filebynamepath(name)
        try: os.mkdir(this_path)
        except FileExistsError: print(f"Ошибка: директория существует")
        except FileNotFoundError: os.makedirs(this_path)


    def rmdir(self, name: str):
        this_path = self.depot.filebynamepath(name)
        try:
            os.rmdir(this_path)
        except FileNotFoundError: print(f"Ошибка: директории {name} не существует")
        except NotADirectoryError: print(f"Ошибка: файл {name} не является директорией")
        except OSError:
            try: shutil.rmtree(this_path, ignore_errors=False, onerror=None)
            except FileNotFoundError: print(f"Ошибка: директории {name} не существует")
            except NotADirectoryError: print(f"Ошибка: файл {name} не является директорией")

    def rename(self, prevname: str, currname: str):

        path_old = self.depot.filebynamepath(prevname)
        path_new = self.depot.filebynamepath(currname)

        # после воода названия файла проверяем уникальность имени
        try:
            if not os.path.isfile(path_new): os.rename(path_old, path_new)
            else: raise IsADirectoryError
        except FileNotFoundError: print(f"Ошибка: указанного файла не существует")
        except IsADirectoryError: print(f"Ошибка: файл с названием уже существует")


    def ls(self):

        this_path = self.depot.path
        filelist = os.listdir(this_path)
        for i in range(len(filelist)):
            if os.path.isdir(self.depot.filebynamepath(filelist[i])):
                filelist[i] = f"[dir] {filelist[i]}"
            else:
                if os.path.isfile(self.depot.filebynamepath(filelist[i])):
                    filelist[i] = f"[file] {filelist[i]}"

        r = '\n'.join(filelist)
        print(f"{this_path}:\n{r}")


    def touch(self, name: str):
        
        # новый пустой файл
        this_path = self.depot.filebynamepath(name)
        try:
            open(this_path, "a").close()
        except IsADirectoryError:
            print(f"Ошибка: файл уже был создан и это директория")


    def cat(self, name: str) -> str:
        
        this_path = self.depot.filebynamepath(name)
        try:
            with open(this_path, "r") as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Ошибка: файл не найден")
        except IsADirectoryError:
            print(f"Ошибка: файл является директорией")


    def rm(self, name: str):
        path = self.depot.filebynamepath(name)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f"Ошибка: файла не существует")


    def cp(self, name: str, path: str):

        path_old = self.depot.filebynamepath(name)
        # выше
        if ".." in path:
            path_new = self.depot.upper_path + self.sep + name
        else:
            # проверка типа
            buff = self.depot.filebynamepath(path)

            # копируем, заранее определив: уровень тот же или другой
            if os.path.isdir(buff):
                path_new = self.depot.filebynamepath(path + self.sep + name)
            else:
                path_new = self.depot.filebynamepath(path)
        try:
            shutil.copyfile(path_old, path_new)
        # копирование папкт
        except IsADirectoryError:
            shutil.copytree(path_old, path_new)
        except FileNotFoundError:
            print(f"Ошибка: файл не найден")

    def mv(self, name: str, path: str):

        path_old = self.depot.filebynamepath(name)
        if ".." in path:
            path_new = self.depot.upper_path + self.sep + name
        else:
            # Проверяем на то, что это за тип файла
            buff = self.depot.filebynamepath(path)
            # Если директория - закидываем туда файл
            if os.path.isdir(buff):
                path_new = self.depot.filebynamepath(path + self.sep + name)
            else:
                # Значит это перемещение на одном уровне
                path_new = self.depot.filebynamepath(path)
        try:
            shutil.move(path_old, path_new)
        except FileNotFoundError:
            print(f"Ошибка: файл не найден")

    def write(self, name: str, *data: str):
        text = " ".join(data)
        path = self.depot.filebynamepath(name)
        try:
            with open(path, "a") as file:
                file.write(text)
        except IsADirectoryError:
            print(f"Ошибка: файл является директорией")

    def router(self, command: str):
        
        # связываем названия команд и соответствующие им функции

        commands = [
            self.cd,
            self.ls,
            self.mkdir,
            self.rmdir,
            self.touch,
            self.rename,
            self.cat,
            self.rm,
            self.cp,
            self.mv,
            self.write,
        ]
        items = dict(zip(FileProcessor.get_cmds().keys(), commands))
        return items.get(command, None)