from django.urls import path
from . import views


urlpatterns = [
    path('tools/row_to_column', views.row_to_column, name='row_to_column'),
    path('tools/column_to_row', views.column_to_row, name='column_to_row'),
    path('tools/delete_duplicates', views.delete_duplicates, name='delete_duplicates'),
    path('tools/numbers_in_words', views.numbers_in_words, name='numbers_in_words')
]