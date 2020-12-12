from django.db import models


class InputResult(models.Model):
    """
    Superclass for models with two fields: input and output
    """
    input_data = models.TextField()
    result = models.TextField()

    def __str__(self):
        return self.input_data


class RowToColumn(InputResult):
    """
    sep: separate char
    """
    sep = models.CharField(max_length=10)


class ColumnToRow(RowToColumn):
    pass


class DeleteDuplicates(InputResult):
    """
    delete_nulls: delete empty or None values from object
    """
    case_sensitive = models.BooleanField(default=False)
    delete_nulls = models.BooleanField(default=False)


class NumbersInWords(InputResult):
    pass


class ListSorting(InputResult):
    case_sensitive = models.BooleanField(default=False)
    reverse = models.BooleanField(default=False)


class ChangeCase(InputResult):
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
    pass


class CrossMinusCleaner(InputResult):
    pass


class UtmDeleter(InputResult):
    pass