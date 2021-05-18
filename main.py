import functools


@functools.total_ordering
class Version:
    version_values = {
        'alpha': '0',
        'beta': '1',
        'rc': '2',
        'r': '3',
        'a': '0',
        'b': '1'
    }

    def __init__(self, version):
        self.version = self.version_normalization(version)

    def version_normalization(self, version: str):
        version = version.replace('-', '.')  # заменяем все "-" на "."
        for ver in self.version_values.keys():  # цикл по ключам словаря со значениями версий
            index = version.find(ver)  # ищем, есть ли в строке словесный номер версии
            if index != -1:  # если такой номер найден
                if version[index - 1] != '.':  # проверяем, есть ли перед ним разделитель "."
                    version = version[:index] + '.' + version[index:]  # если разделителя нету, добавляем его
            version = version.replace(ver, self.version_values[ver])  # заменяем словесный номер версии на числовой
        return version

    def __eq__(self, other):
        return self.version == other.version

    def __lt__(self, other):
        ver1 = self.version.split('.')  # разбиваем значение 1-й версии на элементы по "."
        ver2 = other.version.split('.')  # разбиваем значение 2-й версии на элементы по "."
        min_len = min(len(ver1), len(ver2))  # находим мин. кол-во элементов в 1-й и 2-й версии
        if ver1[:min_len] == ver2[:min_len]:  # проверяем, совпадают ли элементы в мин. кол-ве
            if len(ver1) < len(ver2):  # если элем. равны, то меньше версия с меньшим кол-ом элементов
                return True
        else:  # если жи элементы не равны, то сравниваем поочередно элем. 1-й и 2-й версии
            for i in range(min_len):
                if int(ver1[i]) < int(ver2[i]):
                    return True
                elif int(ver1[i]) > int(ver2[i]):
                    return False
        return False


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0", "1.0.0-rc.1"),
        # ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()