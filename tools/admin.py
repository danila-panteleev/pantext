from django.contrib import admin
from .models import (RowToColumn,
                     ColumnToRow,
                     DeleteDuplicates,
                     NumbersInWords)


@ admin.register(RowToColumn)
class AdminProcessedText(admin.ModelAdmin):
    list_display = ('input_data', 'sep', 'result')


@ admin.register(ColumnToRow)
class AdminProcessedText(admin.ModelAdmin):
    list_display = ('input_data', 'sep', 'result')


@ admin.register(DeleteDuplicates)
class AdminProcessedText(admin.ModelAdmin):
    list_display = ('input_data', 'case_sensitive', 'result')


@ admin.register(NumbersInWords)
class AdminProcessedText(admin.ModelAdmin):
    list_display = ('input_data', 'result')


