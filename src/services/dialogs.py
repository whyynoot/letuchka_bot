from enum import Enum
from typing import List, Union
import uuid
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import shuffle

from ..models.group import Group
from ..models.test import Test, TestQuestion
from ..models.user import Student

TEST_QUESTION_ID = uuid.uuid4()

class DialogAnswerText():
    def __init__(self, messages: Union[str, List[str]], id = None):
        if type(messages) is str:
            self.messages = [messages]
        else:
            self.messages = messages
        if (id):
            self.id = id
        else:
            self.id = uuid.uuid4()
class DialogAnswer():
    def __init__(self, text: DialogAnswerText, markup: ReplyKeyboardMarkup = ReplyKeyboardRemove()):
        self.text = text
        self.markup = markup

class TutorDialogOptions(Enum):
    SETTINGS = "Настроить бота"
    TEST = "Начать летучку"
    CHECK = "Проверить летучки"

class TutorSettingsBranchOptions(Enum):
    TESTS = "Загрузить летучки"
    DATABASE = "Очистить базу"
    GROUP_ADD = "Добавить группы"
    DELETE_GROUP = 'Удалить группу'
    DELETE_STUDENT = 'Удалить ученика'
    CLOSE_GROUP = 'Закрыть набор'
    OPEN_GROUP = 'Открыть набор'
    DELETE_TESTS = 'Удалить летучки'

class TutorSettingsEnterTestsOptions(Enum):
    FINISH = "Загрузил все летучки"

class TutorSettingsClearDatabaseOptions(Enum):
    CONFIRM = "Да, удалить всё!"
    DECLINE = "Нет, я передумал"
class TutorSettingsClearTestOptions(Enum):
    CONFIRM = "Да, удалить всё!"
    DECLINE = "Нет, я передумал"
class TutorTestSuccessOptions(Enum):
    STOP = "Остановить летучку"
class TutorStartDialog(Enum):
    HELLO = DialogAnswerText("Здравствуйте \nЧто необходимо сделать?")

class TutorSettingsBranch(Enum):
    CHOOSE_OPTION = DialogAnswerText("Выберите, что хотите настроить")
    ENTER_GROUPS = DialogAnswerText("Введите группы этого семестра списком (элементы разделяйте переносом строки)")
    ENTER_DELETE_GROUP = DialogAnswerText("Выберите группу для удаления")
    ENTER_DELETE_STUDENT = DialogAnswerText("Выберите ученика для удаления")
    ENTER_OPEN_GROUP = DialogAnswerText("Выберите группу для открытия набора")
    ENTER_CLOSE_GROUP = DialogAnswerText("Выберите группу для закрытия набора")
    ENTER_TESTS = DialogAnswerText("Загрузите файлы с летучками по этому шаблону. Будьте внимательны, название файла будет названием летучки.")
    MORE_TESTS = DialogAnswerText("Вы можете загрузить ещё файлы, либо завершить настройку.")
    CLEAR_DATABASE = DialogAnswerText("Вы точно хотите удалить все данные из базы?")
    DELETE_TESTS = DialogAnswerText("Вы точно хотите удалить все данные из базы?")
    CLEAR_DATABASE_SUCCESS = DialogAnswerText("База успешно очищена, можно заново настраивать бота.")
    CLEAR_DATABASE_DECLINE = DialogAnswerText("Хорошо, не будем очищать базу.")
    DELETE_TESTS_SUCCESS = DialogAnswerText("Летучки удалены")
    DELETE_TESTS_DECLINE = DialogAnswerText("Все осталось на своих местах!")
    FILE_FORMAT_ERROR = DialogAnswerText("Пришлите файл в формате .xlsx")
    SUCCESS = DialogAnswerText("Настройка завершена")
    
class TutorTestBranch(Enum):
    SELECT_TEST = DialogAnswerText("Выберите летучку")
    SELECT_GROUP = DialogAnswerText("Выберете группу")
    SUCCESS = DialogAnswerText(["Летучка началась", "Можете остановить летучку кнопкой ниже"])
    FINISH = DialogAnswerText("Летучка завершена!")

class TutorGroupBranch(Enum):
    SELECT_GROUP = DialogAnswerText("Выберете группу")
    SUCESS = DialogAnswerText("Действие выполнено успешно")
    DECLINE = DialogAnswerText("Не получилось выполнить действие, повторите.")

class TutorCheckBranch(Enum):
    SEND_FILE = DialogAnswerText("Оцените результаты, выставьте баллы в соответствующую графу и пришлите изменённый файл в ответном сообщении")
    SUCCESS = DialogAnswerText("Летучка оценена, результат направлен студентам")

class StudentSettingsBranch(Enum):
    SELECT_GROUP = DialogAnswerText("Привет!\nИз какой ты группы?")
    ENTER_FIO = DialogAnswerText("Введи своё ФИО")
    SUCCESS = DialogAnswerText(["Добро пожаловать в Летучий бот. Здесь ты будешь выполнять летучки по предмету МППР", "Жди сообщения о начале летучки"])

class StudentExistsBranch(Enum):
    NO_TEST = DialogAnswerText("Пока летучки нет - отдыхай, я тоже отдохну")

class StudentTestBranch(Enum):
    FINISH = DialogAnswerText("Ты ответил на все вопросы. Молодец!")
    ABORT = DialogAnswerText("Летучка завершена.\nРезультат ты получишь, как только работу оценит преподаватель")

def create_keyboard(buttons: list[list[str]]):
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

def ask_file(question): #deprecated - Пока не придумал, как использовать для множественных файлов
    answer = yield question
    while not ('.xlsx' in answer.document.file_name):
        answer = yield DialogAnswer(TutorSettingsBranch.FILE_FORMAT_ERROR.value)
    return True

def tutorStartDialog(tests: List[Test], groups: List[Group], students: List[Student]):
    answer = yield DialogAnswer(TutorStartDialog.HELLO.value, create_keyboard([[option.value] for option in TutorDialogOptions]))
    if answer.text == TutorDialogOptions.SETTINGS.value:
        yield from tutor_settings_branch(groups, students)
    elif answer.text == TutorDialogOptions.TEST.value:
        yield from tutor_test_branch(tests, groups)
    else:
        yield from tutor_check_branch()

def tutor_settings_branch(groups: List[Group], students: List[Student]):
    answer = yield DialogAnswer(TutorSettingsBranch.CHOOSE_OPTION.value, create_keyboard([[option.value] for option in TutorSettingsBranchOptions]))
    # Группа добавить
    if answer.text == TutorSettingsBranchOptions.GROUP_ADD.value:
        yield DialogAnswer(TutorSettingsBranch.ENTER_GROUPS.value)
        yield DialogAnswer(TutorSettingsBranch.SUCCESS.value)
    
    # Группы удалить
    elif answer.text == TutorSettingsBranchOptions.DELETE_GROUP.value:
        answer = yield DialogAnswer(TutorSettingsBranch.ENTER_DELETE_GROUP.value, create_keyboard([[group.name] for group in groups]))
        yield DialogAnswer(TutorSettingsBranch.SUCCESS.value)
    
    elif answer.text == TutorSettingsBranchOptions.DELETE_TESTS.value:
        answer = yield DialogAnswer(TutorSettingsBranch.DELETE_TESTS.value, create_keyboard([[option.value for option in TutorSettingsClearDatabaseOptions]]))
        if answer.text == TutorSettingsClearDatabaseOptions.CONFIRM.value:
            yield DialogAnswer(TutorSettingsBranch.DELETE_TESTS_SUCCESS.value)
        if answer.text == TutorSettingsClearDatabaseOptions.DECLINE.value:
            yield DialogAnswer(TutorSettingsBranch.DELETE_TESTS_DECLINE.value)
    
    # Группа открыть набор
    elif answer.text == TutorSettingsBranchOptions.OPEN_GROUP.value:
        answer = yield DialogAnswer(TutorSettingsBranch.ENTER_OPEN_GROUP.value, create_keyboard([[group.name] for group in groups if not group.open]))
        yield DialogAnswer(TutorSettingsBranch.SUCCESS.value)
    
    # Группа закрыть набор
    elif answer.text == TutorSettingsBranchOptions.CLOSE_GROUP.value:
        answer = yield DialogAnswer(TutorSettingsBranch.ENTER_CLOSE_GROUP.value, create_keyboard([[group.name] for group in groups  if group.open]))
        yield DialogAnswer(TutorSettingsBranch.SUCCESS.value)
    
    # Ученик удалить
    elif answer.text == TutorSettingsBranchOptions.DELETE_STUDENT.value:
        answer = yield DialogAnswer(TutorSettingsBranch.ENTER_DELETE_STUDENT.value, create_keyboard([[f"{student.name} | @{student.id}"] for student in students]))
        yield DialogAnswer(TutorSettingsBranch.SUCCESS.value)
    
    # Загрузите летучки
    elif answer.text == TutorSettingsBranchOptions.TESTS.value:
        answer = yield DialogAnswer(TutorSettingsBranch.ENTER_TESTS.value, create_keyboard([[option.value for option in TutorSettingsEnterTestsOptions]]))
        while not(answer.text == TutorSettingsEnterTestsOptions.FINISH.value):
            answer = yield DialogAnswer([])
        yield DialogAnswer(TutorSettingsBranch.SUCCESS.value)

    # Очистить базу данных, вы уверены?
    elif answer.text == TutorSettingsBranchOptions.DATABASE.value:
        answer = yield DialogAnswer(TutorSettingsBranch.CLEAR_DATABASE.value, create_keyboard([[option.value for option in TutorSettingsClearDatabaseOptions]]))
        if answer.text == TutorSettingsClearDatabaseOptions.CONFIRM.value:
            yield DialogAnswer(TutorSettingsBranch.CLEAR_DATABASE_SUCCESS.value)
        if answer.text == TutorSettingsClearDatabaseOptions.DECLINE.value:
            yield DialogAnswer(TutorSettingsBranch.CLEAR_DATABASE_DECLINE.value)

def tutor_test_branch(tests: List[Test], groups: List[Group]):
    yield DialogAnswer(TutorTestBranch.SELECT_TEST.value, create_keyboard([[test.name] for test in tests]))
    yield DialogAnswer(TutorTestBranch.SELECT_GROUP.value, create_keyboard([[group.name] for group in groups]))
    answer = yield DialogAnswer(TutorTestBranch.SUCCESS.value, create_keyboard([[option.value for option in TutorTestSuccessOptions]]))
    if (answer.text == TutorTestSuccessOptions.STOP.value):
        yield DialogAnswer(TutorTestBranch.FINISH.value)

def tutor_check_branch():
    yield DialogAnswer(TutorCheckBranch.SEND_FILE.value)
    yield DialogAnswer(TutorCheckBranch.SUCCESS.value)

def student_settings_branch(groups: List[Group]):
    yield DialogAnswer(StudentSettingsBranch.SELECT_GROUP.value, create_keyboard([[group.name] for group in groups if group.open]))
    yield DialogAnswer(StudentSettingsBranch.ENTER_FIO.value)
    yield DialogAnswer(StudentSettingsBranch.SUCCESS.value)

def student_exists_branch():
    yield DialogAnswer(StudentExistsBranch.NO_TEST.value)


def student_test_branch(test_name: str, questions: List[TestQuestion]):
    # Mixing questions inccorect answers recieved
    # shuffle(questions)

    yield DialogAnswer(DialogAnswerText(["ВНИМАНИЕ! Начинаем летучку %s" % test_name, "Вопрос %i: %s" % (1, questions[0].text)], TEST_QUESTION_ID))
    for index, question in enumerate(questions[1:]):
        yield DialogAnswer(DialogAnswerText("Вопрос %i: %s" % (index+2, question.text), TEST_QUESTION_ID))
    yield DialogAnswer(StudentTestBranch.FINISH.value)

def student_abort_test():
    yield DialogAnswer(StudentTestBranch.ABORT.value)

def student_check_branch(test_name: str, mark: int, max_mark: int):
    yield DialogAnswer(DialogAnswerText(["Привет!",f'Твоя летучка “{test_name}” оценена\n\nБаллы: {round(mark, 2)}/{max_mark}']))
