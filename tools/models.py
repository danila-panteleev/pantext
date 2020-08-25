from django.db import models


class InputResult(models.Model):
    input_data = models.TextField()
    result = models.TextField()

    def __str__(self):
        return self.input_data


class RowToColumn(InputResult):
    sep = models.CharField(max_length=10)


class ColumnToRow(RowToColumn):
    pass


class DeleteDuplicates(InputResult):
    case_sensitive = models.BooleanField(default=False)
    save_position = models.BooleanField(default=False)


class NumbersInWords(InputResult):
    pass


class ListSorting(InputResult):
    case_sensitive = models.BooleanField(default=False)
    save_position = models.BooleanField(default=False)