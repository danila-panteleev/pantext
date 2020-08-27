from django.shortcuts import render
from .forms import (RowToColumnForm,
                    ColumnToRowForm,
                    DeleteDuplicatesForm,
                    NumberInWordsForm,
                    ListSortingForm,
                    ChangeCaseForm)


def row_to_column(request):
    form = RowToColumnForm()
    if request.method == 'POST':
        form = RowToColumnForm(request.POST)

    if form.is_valid():
        form = form.row_to_column()
        form = RowToColumnForm(form.cleaned_data)
        form.save()

    context = {
        'form': form,
    }

    return render(request, 'tools/row_to_column.html', context)


def column_to_row(request):
    form = ColumnToRowForm()
    if request.method == 'POST':
        form = ColumnToRowForm(request.POST)

    if form.is_valid():
        form = form.column_to_row()
        form = ColumnToRowForm(form.cleaned_data)
        form.save()

    context = {
        'form': form,
    }

    return render(request, 'tools/column_to_row.html', context)


def delete_duplicates(request):
    form = DeleteDuplicatesForm()
    if request.method == 'POST':
        form = DeleteDuplicatesForm(request.POST)

    if form.is_valid():
        case_sensitive = request.POST.getlist('case_sensitive')
        delete_nulls = request.POST.getlist('delete_nulls')
        form = form.delete_duplicates(case_sensitive=case_sensitive,
                                      delete_nulls=delete_nulls)
        form = DeleteDuplicatesForm(form.cleaned_data)
        form.save()

    context = {
        'form': form,
    }

    return render(request, 'tools/delete_duplicates.html', context)


def numbers_in_words(request):
    form = NumberInWordsForm()
    if request.method == 'POST':
        form = NumberInWordsForm(request.POST)

    if form.is_valid():
        form = form.numbers_in_words()
        form = NumberInWordsForm(form.cleaned_data)
        form.save()

    context = {
        'form': form,
    }
    return render(request, 'tools/numbers_in_words.html', context)


def list_sorting(request):
    form = ListSortingForm()
    if request.method == 'POST':
        form = ListSortingForm(request.POST)

    if form.is_valid():
        case_sensitive = request.POST.getlist('case_sensitive')
        reverse = request.POST.getlist('reverse')
        form = form.sorting(case_sensitive=bool(case_sensitive),
                            reverse=bool(reverse))
        form = ListSortingForm(form.cleaned_data)
        form.save()

    context = {
        'form': form,
    }
    return render(request, 'tools/list_sorting.html', context)


def change_case(request):
    form = ChangeCaseForm()
    if request.method == 'POST':
        form = ChangeCaseForm(request.POST)

    if form.is_valid():
        form = form.change_case()
        form = ChangeCaseForm(form.cleaned_data)
        form.save()

    context = {
        'form': form,
    }
    return render(request, 'tools/change_case.html', context)