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
    save_position = models.BooleanField(default=False)


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
    save_position = models.BooleanField(default=False)


class ChangeCase(InputResult):
    """
    Модель для формы "Изменение регистра
    """
    pass