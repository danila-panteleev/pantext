from django import forms
from .models import (InputResult,
                     RowToColumn,
                     ColumnToRow,
                     DeleteDuplicates,
                     NumbersInWords)
from ru_number_to_text.num2t4ru import decimal2text, num2text
import decimal


class InputForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        self.fields['result'].required = False

    class Meta:
        model = InputResult
        fields = ['input_data', 'result']
        widgets = {
            'input_data': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Вставьте текст',
            }),
            'result': forms.Textarea(attrs={
                'readonly': True,
                'class': 'form-control'
            }),

        }


class RowToColumnForm(InputForm):
    class Meta(InputForm.Meta):
        model = RowToColumn

        fields = list(InputForm.Meta.fields)
        fields.extend(['sep'])

        widgets = dict(InputForm.Meta.widgets)
        widgets.update({
            'sep': forms.TextInput(attrs={
                'placeholder': 'Вставьте разделитель',
                'class': 'mt-3 mb-3'})
        })

    def row_to_column(self):
        if self.is_valid():
            result = self.cleaned_data['input_data'].split(self.cleaned_data['sep'])

            for i in range(len(result)):
                result[i] = result[i].strip()

            self.cleaned_data['result'] = '\n'.join(result).strip()

        return self


class ColumnToRowForm(RowToColumnForm):
    def __init__(self, *args, **kwargs):
        super(ColumnToRowForm, self).__init__(*args, **kwargs)
        self.fields['sep'].strip = False

    class Meta(RowToColumnForm.Meta):
        model = ColumnToRow

    def column_to_row(self):
        if self.is_valid():
            result = self.cleaned_data['input_data'].split('\n')

            for i in range(len(result)):
                result[i] = result[i].strip()

            self.cleaned_data['result'] = self.cleaned_data['sep'].join(result)

        return self


class DeleteDuplicatesForm(InputForm):
    def __init__(self, *args, **kwargs):
        super(DeleteDuplicatesForm, self).__init__(*args, **kwargs)
        self.fields['case_sensitive'].required = False
        self.fields['delete_nulls'].required = False

    case_sensitive = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'label': 'case_sensitive',
        'name': 'case_sensitive',
        'checked': True
    }))

    delete_nulls = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'label': 'delete_nulls',
        'name': 'delete_nulls',
        'checked': True
    }))

    class Meta(InputForm.Meta):
        model = DeleteDuplicates

    def delete_duplicates(self, case_sensitive=False, delete_nulls=True):
        if self.is_valid():
            result = self.cleaned_data['input_data'].split('\n')

            for i in range(len(result)):
                result[i] = result[i].strip()
                if not case_sensitive:
                    result[i] = result[i].lower()

            temp = [result[0]]
            for i in range(1, len(result)):
                if result[i] in temp:
                    result[i] = ''
                else:
                    temp.append(result[i])

            if delete_nulls:
                result = list(filter(bool, result))

            print(result)
            self.cleaned_data['result'] = '\n'.join(result)

        return self


class NumberInWordsForm(InputForm):
    class Meta(InputForm.Meta):
        model = NumbersInWords

    def numbers_in_words(self, with_cents=False, currency=''):
        if self.is_valid():
            result = self.cleaned_data['input_data']

            if with_cents:
                try:
                    result = decimal2text(decimal.Decimal(result))
                except decimal.InvalidOperation:
                    result = result.replace(',', '.')
                    result = ''.join(
                        list(filter(lambda x: x in '1234567890.', result))
                    )
                    if result.count('.') > 1:
                        result = result.split('.')
                        result_head = ''.join(result[:-1])
                        result = result_head + '.' + result[-1]
                        result = decimal2text(decimal.Decimal(result))
                except IndexError:
                    result = f'Я пока не умею обрабатывать числа больше 999,999,999,999.99 ' \
                             f'({num2text(999999999999.99)}'
            else:
                try:
                    result = num2text(int(result))
                except ValueError:
                    result = (''.join(
                        list(
                            filter(
                                lambda x: x.isnumeric(),
                                result
                            )
                        )
                    ))
                    result = num2text(int(result))
                except IndexError:
                    result = f'Я пока не умею обрабатывать числа больше 999 999 999 999 ' \
                             f'({num2text(999999999999)}'

            result = result.capitalize()
            if currency:
                pass
            self.cleaned_data['result'] = result
        return self
