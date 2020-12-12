from django.db import models


class InputResult(models.Model):
    """
    Суперкласс для моделей, состоящих из двух полей: ввод и вывод
    """
    input_data = models.TextField()
    result = models.TextField()

    def __str__(self):
        return self.input_data


class RowToColumn(InputResult):
    """
    Модель для формы "Строка в столбец"
    """
    sep = models.CharField(max_length=10)


class ColumnToRow(RowToColumn):
    """
    Модель для формы "Столбец в строку"
    """
    pass


class DeleteDuplicates(InputResult):
    """
    Модель для формы "Удаление дубликатов"
    """
    case_sensitive = models.BooleanField(default=False)
    delete_nulls = models.BooleanField(default=False)


class NumbersInWords(InputResult):
    """
    Модель для формы "Число прописью"
    """
    pass


class ListSorting(InputResult):
    """
    Модель для формы "Сортировка списка"
    """
    case_sensitive = models.BooleanField(default=False)
    reverse = models.BooleanField(default=False)


class ChangeCase(InputResult):
    """
    Модель для формы "Изменение регистра"
    """
    EACH_WORD = 'each_word'
    SENTENCE = 'sentence'
    ALL_LETTERS = 'all_letters'
    FENCE = 'fence'
    RANDOM_CASE = 'random_case'

    MODE_CHOICES = [
        (EACH_WORD, 'Каждое Слово / кАЖДОЕ сЛОВО'),
        (SENTENCE, 'Как. В предложении'),
        (ALL_LETTERS, 'ВСЕ БУКВЫ / все буквы'),
        (FENCE, 'ЗаБоРчИкОм'),
        (RANDOM_CASE, 'сЛуЧАЙныЙ РЕГиСТр')
    ]

    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default=EACH_WORD)
    option_reverse = models.BooleanField(default=False)
    option_force = models.BooleanField(default=False)


class Autofill(InputResult):
    """
    Модель для формы "Автозаполнение строк"
    """


class CrossMinusCleaner(InputResult):
    """
    Модель для формы "Чистка от кросс-минусации"
    """


class UtmDeleter(InputResult):
    """
    Модель для формы "Чистка от UTM-меток"
    """