import json
import os
from datetime import datetime
from functools import wraps


class User:
    """Класс учета пользователей

    Attributes:
        name (str): Имя пользователя
        history (list): Лист с объектами трат

    Methods:
        add_cost(cost): Добавляет затраты пользователю
        get_users(): Возвращает созданные экземляры класса User
        delete(): Удаляет сохраненные экземпляры класса User
        to_dict(): Превращает все экземпляры класса в словари
        from_dict(data): Превращает словарь в экземпляр класса User и добавляет список трат
    """
    __users = []

    def __init__(self, name):
        self.__name = name
        self.__history = []
        __class__.__users.append(self)

    @property
    def name(self):
        return self.__name

    @property
    def history(self):
        """Выводит историю трат пользователя"""
        return self.__history

    def add_cost(self, cost):
        """Добавление затраты пользователю

        Args:
            cost (obj): Объект расхода
        """
        self.__history.append(cost)

    @classmethod
    def get_users(cls):
        """Возвращает созданные экземляры класса User"""
        return cls.__users

    @classmethod
    def delete(cls):
        """Удаляет сохраненные экземляры класса User"""
        cls.__users.clear()

    @classmethod
    def to_dict(cls):
        """Возвращает лист со словарями атрибутов экземпляров"""
        list_user = []
        for user in cls.__users:
            list_id = []
            for number in user.__history:
                list_id.append(number.id)

            user_dict = {'name': user.__name,
                         'id': list_id}

            list_user.append(user_dict)
        return list_user

    @classmethod
    def from_dict(cls, data):
        """Превращает словарь в объект пользователя
        и привязывает объекты трат
        """
        user = cls(data['name'])
        for id in data['id']:
            user.add_cost(Expense.specimens()[id])
        return user


class Expense:
    """Класс для учета расходов

    Attributes:
        category (str): Категория расхода
        cost (int/float): Величина расхода
        date (str): Дата совершения расхода
        id (int): Id затраты

    Methods:
        specimens(): Получить список всех расходов
        delete(): Удалить список всех расходов
        get_category(): Получить список всех категорий
        to_dict(): Превратить все экземляры в словарь для сохранения
        from_dict(dictionary): Превратить словарь в экземляр класса
    """
    __tuple_category = ('Не задано', 'Жилье', 'Продукты',
                        'Одежда и обувь', 'Развлечения',
                        'Транспорт', 'Медицина', 'Инвестиции')
    __specimens = []

    def __init__(self, category, cost, date):
        self.__category = category
        self.__cost = cost
        self.__date = date
        self.__id = len(__class__.__specimens)
        __class__.__specimens.append(self)

    @classmethod
    def specimens(cls):
        return cls.__specimens

    @classmethod
    def delete(cls):
        """Удаляет сохраненные экземляры класса"""
        cls.__specimens.clear()

    @classmethod
    def get_category(cls):
        """Получить список всех категорий"""
        return cls.__tuple_category

    @property
    def category(self):
        """Выводит категорию затрат"""
        return __class__.__tuple_category[self.__category]

    @category.setter
    def category(self, category):
        self.__category = __class__.__valiable_category(category)

    @property
    def cost(self):
        """Возвращает значение затраты"""
        return self.__cost

    @cost.setter
    def cost(self, value):
        self.__cost = __class__.__valiable_cost(value)

    @property
    def date(self):
        """Выводит дату затраты"""
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = __class__.__valiable_date(value)

    @property
    def id(self):
        """Выводит id затраты"""
        return self.__id

    @classmethod
    def to_dict(cls):
        """Превращает затраты в лист словарей для хранения"""
        list_dictionaries = []
        for copy in cls.__specimens:
            list_dictionaries.append({'id': copy.__id,
                                      'category': copy.__category,
                                      'cost': copy.__cost,
                                      'date': copy.__date
                                      })
        return list_dictionaries

    @classmethod
    def from_dict(cls, dictionary):
        """Превращает словарь с затратами в объект"""
        expence = cls(dictionary['category'],
                      dictionary['cost'], dictionary['date']
                      )

        expence.__category = dictionary['category']
        return expence


class Save:
    """Класс сохранения и загрузки пользователей и их расходов

    Methods:
        __path_project(): Возвращает путь для сохранения или создает новый путь
        dump(): Сохраняет пользователей и траты в json файлах
        load(): Загружает пользователей и траты из json файлов
    """
    @classmethod
    def dump(cls):
        """Сохраняет траты в формате json"""
        costs = Expense.to_dict()
        path_expence, path_users = cls.__path_project()

        with open(path_expence, 'w', encoding='utf-8') as file:
            json.dump(costs, file, ensure_ascii=False, indent=4)

        users = User.to_dict()
        with open(path_users, 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls):
        """Загружает затраты и пользователей и вызывает
        from_dict() классов Expense и User для создания объектов
        """
        User.delete()
        Expense.delete()

        path_expence, path_users = cls.__path_project()

        try:
            with open(path_expence, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for cost in data:
                    Expense.from_dict(cost)

            with open(path_users, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for user in data:
                    User.from_dict(user)
        except FileNotFoundError:
            pass

    @staticmethod
    def __path_project():
        """Создает путь для сохранения файлов

        Returns:
            path_expence (str): Полный путь к хранению затрат
            path_users (str): Полный путь к хранению пользователей
        """
        path = os.path.dirname(__file__)
        data_path = os.path.join(path, 'data')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        path_expence = os.path.join(data_path, 'Expence.json')
        path_users = os.path.join(data_path, 'Users.json')
        return path_expence, path_users


def add_border(func):
    """Добавление границ

    Args:
        func (any): Функция, по началу и окончании которой, будут добавлены границы
    """
    @wraps(func)
    def wrapper(*args, **quargs):
        print()
        print('=' * 50)
        data = func(*args, **quargs)
        print('=' * 50)
        return data
    return wrapper


def check_cancel(func):
    """Проверка является ли значение Отмена или Недопустимым

    Args:
        func (any): Функция, результат которой будет проверен на значение 'Отмена' и 'None'

    Returns:
        func (any): Изначальная функция
    """
    @wraps(func)
    def wrapper(*args, **quargs):
        check = func(*args, **quargs)
        if check == 'Отмена':
            print("Действие отменено")
        if check is None:
            print(f"Недопустимое значение, попробуйте снова")
        return check
    return wrapper


class ConsoleInput:
    """Класс для ввода информации о затратах с консоли

    Methods:
        input_category(): Ввод информации о категории
        __is_valiable_category(category, type): Проверка допустимости введеной категории
        input_cost(): Ввод информации о значении траты
        input_date(): Ввод информации о дате траты
    """
    @classmethod
    @add_border
    @check_cancel
    def input_category(cls):
        """Ввод категории пользователем

        Returns:
            Отмена (str): При вводе отмена
            category (str): При допустимой категории
            None : При недопустимой категории
        """
        categories = Expense.get_category()

        print("Список доступных категорий:")
        id = 1
        for category in categories:
            print(f"{id}) {category}")
            id += 1

        i_category = input("Введите индекс категории или категорию: ")
        try:
            i_category = cls.__is_valide_category(int(i_category), int)
        except ValueError:
            i_category = cls.__is_valide_category(i_category, str)
        return i_category

    @staticmethod
    def __is_valide_category(category, type):
        """Проверяет допустимость категории

        Args: 
            category (int, str): Введеная категория для проверки
            type (int, str) : Тип направленного аргумента category

        Returns:
            Отмена (str): При вводе отмена
            сategory (str): При допустимой категории
            None : При недопустимой категории
        """
        categoties = Expense.get_category()
        if type is int:
            if 1 <= category <= len(categoties):
                category = category - 1
            else:
                return None
        elif type is str:
            if category.capitalize() == 'Отмена':
                return 'Отмена'
            try:
                category = categoties.index(category.capitalize())
            except ValueError:
                return None
        print(f"Выбрана категория '{categoties[category]}'")
        return category

    @staticmethod
    @add_border
    @check_cancel
    def input_cost():
        """Ввод затрат пользователем

        Returns:
            i_cost (float): Величина затрат введеная пользователем
            None: При вводе недопустимого значения
            Отмена (str): При отмене действия
        """
        i_cost = input("Введите величину затрат: ")
        try:
            i_cost = float(i_cost)
            print(f"Величина затрат составляет {i_cost} рублей")
            return i_cost
        except ValueError:
            if i_cost.capitalize() == "Отмена":
                return "Отмена"
            return None

    @staticmethod
    @add_border
    @check_cancel
    def input_date():
        """Ввод даты затраты пользователем

        Returns:
            i_date (str): Дата затраты введеная пользовтелем
            Отмена (str): При отмене действия
            None: При недопустимом значении
        """
        i_date = input("Введите дату затраты: ")
        try:
            i_date = datetime.strptime(i_date, "%d.%m.%Y").strftime("%d.%m.%Y")
            print(f"Выбранная дата '{i_date}'")
            return i_date
        except ValueError:
            if i_date.capitalize() == 'Отмена':
                return 'Отмена'
            return None

    @classmethod
    @add_border
    def input_user(cls):
        """Выводит список доступных пользователей и просит ввести нужного

        Returns:
            user (obj): Выбранный пользователь  
            None: При недопустимом значении
        """
        users = User.get_users()
        id = 1
        print("Список доступных пользователей:")
        for user in users:
            print(f"{id}) {user.name}")
            id += 1
        input_user = input(
            "Введите индекс нужного пользователя или его имя: ").capitalize()
        input_user = cls.__is_valiable_user(input_user, users)
        return input_user

    @staticmethod
    @add_border
    def answer_about_add_user():
        """Задает вопрос пользователю о добавлении нового пользователя

        Returns:
            True (bool): При ответе Да  
            False (bool): При любом другом ответе
        """
        print(f"Хотите ли вы добавить нового пользователя?" +
              f"\nПри ответе 'Да' будет добавлен новый пользователь")
        question = input("Введено: ").capitalize()
        if question == 'Да':
            return True
        return False

    @staticmethod
    @check_cancel
    def __is_valiable_user(user, users):
        """Проверяет наличие пользователя, при отсутсвии спрашивает добавить ли нового

        Args:
            user (str): Пользователь введеный пользователем
            users (list): Список допустимых объектов пользователей

        Returns:
            user (obj): Выбранный пользователь  
            Отмена (str): При отмене действия   
            None: При недопустимом значении
        """
        try:
            if 1 <= int(user) <= len(users):
                return users[int(user)-1]
        except ValueError:
            if user == 'Отмена':
                return 'Отмена'
            for one_user in users:
                if user == one_user.name:
                    return one_user
            return None

    @classmethod
    @add_border
    def add_user(cls):
        """Ввод имени нового пользователя

        Returns:
            new_user(str): Новый пользователь
            None: Недопустимое имя или отмена дейтсвия
        """
        new_user = input("Введите имя нового пользователя: ").capitalize()
        new_user = cls.__is_valid_new_user(new_user)
        if new_user == None:
            print("Действие отменено")
        return new_user

    @staticmethod
    def __is_valid_new_user(user):
        """Проверяет допустимость имени нового пользователя

        Returns:
            user(str): Допустимое имя пользователя
            None: Введена пустая строка или Отмена
        """
        if len(user) == 0 or user == 'Отмена':
            return None
        return user

    @classmethod
    @add_border
    def input_command(cls, command_dict):
        """Показывает список доступных действий и просит ввести действие

        Args:
            command_dict (dict): Словарь со всеми доступными действиями

        Returns:
            command (str): Введеное пользователем действие  
            Отмена (str): При отмене действия   
            None: При недопустимом значении
        """
        print("Список доступных действий:")
        commands = command_dict.keys()
        id = 1
        for command in commands:
            print(f"{id}) {command}")
            id += 1
        command = input("Введите нужную команду или индекс нужной команды: ")
        command = cls.__is_valiable_command(command, commands)
        return command

    @staticmethod
    @check_cancel
    def __is_valiable_command(command, dict_key_command):
        """Проверяет допустимость команды

        Args:
            command (str): Команда введеная пользователем
            dict_key_command (dict): Список допустимых команд

        Returns:
            сommand (str): Введеное пользователем действие  
            Отмена (str): При отмене действия   
            None: При недопустимом значении
        """
        try:
            if 1 <= int(command) <= len(dict_key_command):
                list_commands = []
                for one_command in dict_key_command:
                    list_commands.append(one_command)
                return list_commands[int(command) - 1]
        except ValueError:
            if command.capitalize() in dict_key_command:
                return command.capitalize()
            elif command.capitalize() == 'Отмена':
                return 'Отмена'
        return None


class ConsoleOutput:
    """Класс вывода информации в консоль"""
    @staticmethod
    def result_none(date):
        """Вывод результат не найден

        Args:
            date (str): Дата, на которую был поиск затрат
        """
        print(f"На '{date}' отсутвует информация о тратах")

    @staticmethod
    def result_print(list_result):
        """Вывод результатов

        Args:
            list_result (list): Лист, с результатами для вывода
        """
        print("Найденные результаты:")
        id = 1
        for cost in list_result:
            print(f"{id}) Трата в размере {cost.cost} в категории '{cost.category}'")
            id += 1


class Search:
    """Класс работы с данными

    Methods:
        seek_day(user, day): Ищет затраты пользователя за день
    """
    @staticmethod
    def seek_day(user, day):
        """Проверяет и возвращает затраты за день пользователя

        Args:
            user (obj): Пользователь, у которого будет поиск затрат
            day (str): День, за который будут выводиться затраты

        Returns:
            find_costs (list): Лист, в котором собраны затраты за нужный день
            None: В нужный день затраты не найдены
        """
        find_costs = []
        data = user.history
        for cost in data:
            if cost.date == day:
                find_costs.append(cost)
        if len(find_costs) == 0:
            return None
        return find_costs


class Main_logic:
    """Класс управления программой

    Attributes:
        commands_dict(dict): Возвращает словарь всех доступных действий

    Methods:
        manager_progect(): Главный метод управления программой
        choose_user(): Выбор пользователя
        choose_command(): Выбор команды
        add_cost(user): Добавляет новую затрату пользователю
        check_cost(user): Производит поиск затрат по дате
    """

    def __init__(self):
        self.__commands_list = {'Добавить затраты': self.add_cost,
                                'Проверить затраты': self.check_cost}

        Save.load()
        self.manager_progect()

    def manager_progect(self):
        """Главное управление проектом"""
        user = self.choose_user()
        if user is None:
            return

        while True:
            command = self.choose_command()
            if command is None:
                return
            active = self.__commands_list[command](user)
            if active is False:
                continue

    def choose_user(self):
        """Выбор пользователя, при отсутсвии нужного предлагает ввести нового

        Returns:
            user(obj): Если пользователь выбран 
            None: Если действие отменено
        """
        while True:
            user = ConsoleInput.input_user()
            if user == 'Отмена':
                return None
            elif user == None:
                answer = ConsoleInput.answer_about_add_user()
                if answer:
                    new_user = ConsoleInput.add_user()
                    if new_user is not None:
                        User(new_user)
                continue
            return user

    def choose_command(self):
        """Выбор команды для выполнения

        Returns:
            command(str): Выбранная команда
            None: Если действие отменено
        """
        while True:
            command = ConsoleInput.input_command(self.commands_dict)
            if command == 'Отмена':
                return None
            elif command == None:
                continue
            return command

    @property
    def commands_dict(self):
        """Возвращает словарь доступных действий"""
        return self.__commands_list

    def add_cost(self, user):
        """Добавление затрат

        Args:
            user (obj) : Пользователь, к которому будут добавлены затраты

        Returns:
            None: Успешно выполнено    
            False(bool): Действие отменено
        """
        commands = (ConsoleInput.input_date,
                    ConsoleInput.input_category,
                    ConsoleInput.input_cost,
                    )
        variable = []
        for command in commands:
            while True:
                var = command()
                if var == 'Отмена':
                    return False
                elif var is None:
                    continue
                variable.append(var)
                break
        date, category, cost = variable

        new_cost = Expense(category, cost, date)
        user.add_cost(new_cost)
        Save.dump()

    def check_cost(self, user):
        """Проверка затрат

        Args:
            user (obj): Пользователь для поиска затрат
        """
        while True:
            date = ConsoleInput.input_date()
            if date == 'Отмена':
                return False
            elif date is None:
                continue
            break
        find_costs = Search.seek_day(user, date)
        if find_costs is None:
            ConsoleOutput.result_none(date)
            return
        ConsoleOutput.result_print(find_costs)


m = Main_logic()
