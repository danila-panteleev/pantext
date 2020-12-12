from django import forms
from django.forms import formset_factory
from .models import (InputResult,
                     RowToColumn,
                     ColumnToRow,
                     DeleteDuplicates,
                     NumbersInWords,
                     ListSorting,
                     ChangeCase,
                     Autofill,
                     CrossMinusCleaner,
                     UtmDeleter)
from num2t4ru import decimal2text, num2text
import decimal
import random
import re


class InputForm(forms.ModelForm):
    """
    Суперкласс для форм, состоящих из двух полей: ввод и вывод
    """

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
    """
    Форма "Строка в столбец"
    """

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
    """
    Форма "Столбец в строку"
    """

    def __init__(self, *args, **kwargs):
        super(ColumnToRowForm, self).__init__(*args, **kwargs)
        self.fields['sep'].strip = False
        self.fields['delete_extra_space'].required = False
        self.fields['delete_nulls'].required = False

    delete_extra_space = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input mb-0',
        'label': 'delete_extra_space',
        'name': 'delete_extra_space',
        'checked': True
    }))

    delete_nulls = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'label': 'delete_nulls',
        'name': 'delete_nulls',
        'checked': True
    }))

    class Meta(RowToColumnForm.Meta):
        model = ColumnToRow

    def column_to_row(self, delete_nulls=True, delete_extra_space=True):
        delete_nulls = bool(delete_nulls)
        delete_extra_space = bool(delete_extra_space)
        if self.is_valid():
            result = self.cleaned_data['input_data'].split('\n')
            print(result)

            for i in range(len(result)):
                result[i] = result[i].strip('\r')

            if delete_extra_space:
                for i in range(len(result)):
                    result[i] = result[i].strip('\t')
                    result[i] = result[i].strip(' ')

            if delete_nulls:
                result = list(filter(bool, result))

            self.cleaned_data['result'] = self.cleaned_data['sep'].join(result)

        return self


class DeleteDuplicatesForm(InputForm):
    """
    Форма "Удаление дубликатов"
    """

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
        """
        :param case_sensitive: регистрозависимость
        :param delete_nulls: удаление пустых строк (если False, то все первые значения остаются на своих позициях,
        вместо дублей пустая строка)
        """
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

            # print(result)
            self.cleaned_data['result'] = '\n'.join(result)

        return self


class NumberInWordsForm(InputForm):
    """
    Форма "Число прописью"
    """

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


class ListSortingForm(InputForm):
    """
    Форма "Сортировка списков"
    """

    class Meta(InputForm.Meta):
        model = ListSorting

    def __init__(self, *args, **kwargs):
        super(ListSortingForm, self).__init__(*args, **kwargs)
        self.fields['case_sensitive'].required = False
        self.fields['reverse'].required = False

    case_sensitive = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'label': 'case_sensitive',
        'name': 'case_sensitive',
        'checked': False
    }))

    reverse = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'label': 'reverse',
        'name': 'reverse',
        'checked': False
    }))

    def sorting(self, reverse=False, case_sensitive=False):
        """
        :param reverse: обратный порядок
        :param case_sensitive: регистрозависимость
        """
        if self.is_valid():
            if case_sensitive:
                self.cleaned_data['result'] = '\n'.join(
                    sorted(
                        self.cleaned_data['input_data'].split(),
                        reverse=reverse
                    )
                )
            else:
                # print(self.cleaned_data['input_data'].split())
                self.cleaned_data['result'] = '\n'.join(
                    sorted(
                        self.cleaned_data['input_data'].split(),
                        reverse=reverse,
                        key=str.lower
                    )
                )
        return self


class ChangeCaseForm(InputForm):
    """
    Форма "Изменение регистра"
    """

    class Meta(InputForm.Meta):
        model = ChangeCase

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

    mode = forms.CharField(label='Режим: ', max_length=50,
                           widget=forms.Select(
                               choices=MODE_CHOICES,
                               attrs={
                                   'class': 'form-select',
                                   'label': 'mode',
                                   'name': 'mode',
                               }
                           ))

    option_reverse = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input mt-2 mb-2',
        'label': 'option_reverse',
        'name': 'option_reverse',
        'checked': False
    }))

    option_force = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input mt-2 mb-2',
        'label': 'option_force',
        'name': 'option_force',
        'checked': False
    }))

    def __init__(self, *args, **kwargs):
        super(ChangeCaseForm, self).__init__(*args, **kwargs)
        self.fields['option_reverse'].required = False
        self.fields['option_force'].required = False

    def change_case(self, mode='', option_reverse=True, option_force=True):
        """
        Основная функция изменения регистра

        :param mode: тип изменения регистра(вызываемая подфункция):
                                             Каждое слово           each_word
                                             Как в предложениях     sentence
                                             Все буквы              all_letters
                                             Заборчиком (ПрИмЕр)    fence
                                             Случайный регистр      random_case
        :param option_reverse: если True, то подфункция инвертируется
        :param option_force: если True, то подфункция принудительно меняет регистр
        :return: self
        """
        option_reverse = bool(option_reverse)
        option_force = bool(option_force)

        def each_word(data, reverse=option_reverse, force=option_force):
            """
            Каждое слово

            :param data: строка
            :param reverse: если True, то функция инвертируется
            :param force: если True, то функция принудительно меняет регистр
            :return: итоговая строка
            """
            data = list(data)

            if reverse:
                data[0] = data[0].lower()
            else:
                data[0] = data[0].upper()

            for i in range(1, len(data)):
                if data[i - 1] in [' ', '\n', '\t']:
                    if reverse:
                        data[i] = data[i].lower()
                    else:
                        data[i] = data[i].upper()

                elif force:
                    if reverse:
                        data[i] = data[i].upper()
                    else:
                        data[i] = data[i].lower()

            return ''.join(data)

        def sentence(data, reverse=option_reverse, force=option_force):
            """
            Как в предложениях.
            После знаков препинания и с новой строки (preps) первая буква слова большая

            :param data: строка
            :param force: если True, то функция принудительно изменяет регистр
            :param reverse: если True, то функция инвертируется
            :return: итоговая строка
            """
            data = list(data)
            preps = ['.', '!', '\n', '?']
            if reverse:
                data[0] = data[0].lower()
                data[1] = data[1].upper()
            else:
                data[0] = data[0].upper()

            for i in range(2, len(data)):
                if reverse:
                    if (data[i - 2] not in preps
                            and data[i - 1] not in preps):

                        if not data[i - 1].islower():
                            data[i] = data[i].upper()

                    elif force:
                        data[i] = data[i].upper()

                else:
                    if (data[i - 2] in preps
                            or data[i - 1] in preps):

                        if not data[i - 1].isupper():
                            data[i] = data[i].upper()

                    elif force:
                        data[i] = data[i].lower()

            return ''.join(data)

        def all_letters(data, reverse=option_reverse):
            """
            Все буквы

            :param data: строка
            :param reverse: если True, то функция инвертируется
            :return: итоговая строка
            """

            if reverse:
                data = data.lower()
            else:
                data = data.upper()

            return data

        def fence(data, reverse=option_reverse):
            """
            Заборчик

            :param data: строка
            :param reverse: инверсия
            :return: итоговая строка
            """
            data = list(data)
            preps = ['.', '!', '?', ' ', '\n', '\t', '\r']
            flip = True

            for i in range(len(data)):
                if reverse:
                    if data[i] not in preps:
                        if flip:
                            data[i] = data[i].lower()
                            flip = False
                        else:
                            data[i] = data[i].upper()
                            flip = True
                else:
                    if data[i] not in preps:
                        if flip:
                            data[i] = data[i].upper()
                            flip = False
                        else:
                            data[i] = data[i].lower()
                            flip = True

            return ''.join(data)

        def random_case(data):
            data = list(data)

            for i in range(len(data)):
                if random.choice([True, False]):
                    data[i] = data[i].upper()
                else:
                    data[i] = data[i].lower()

            return ''.join(data)

        if self.is_valid():
            input_data = self.cleaned_data['input_data']

            if mode == 'each_word':
                self.cleaned_data['result'] = each_word(input_data)

            elif mode == 'sentence':
                self.cleaned_data['result'] = sentence(input_data)

            elif mode == 'all_letters':
                self.cleaned_data['result'] = all_letters(input_data)

            elif mode == 'fence':
                self.cleaned_data['result'] = fence(input_data)

            elif mode == 'random_case':
                self.cleaned_data['result'] = random_case(input_data)

        return self


class AutofillForm(InputForm):
    """
    Форма "Автозаполнение пустых строк"
    """

    class Meta(InputForm.Meta):
        model = Autofill

    def __init__(self, *args, **kwargs):
        super(AutofillForm, self).__init__(*args, **kwargs)
        self.fields['input_data'].strip = False

    def autofill(self):

        if self.is_valid():
            input_data = self.cleaned_data['input_data'].split('\r')
            temp = input_data[0].strip()
            for i in range(1, len(input_data)):
                if input_data[i] == '\n':
                    input_data[i] = temp
                else:
                    input_data[i] = input_data[i].strip()
                    temp = input_data[i]
        self.cleaned_data['result'] = '\n'.join(input_data)
        return self


class CrossMinusCleanerForm(InputForm):
    class Meta(InputForm.Meta):
        model = CrossMinusCleaner

    def cross_minus_delete(self):
        if self.is_valid():
            input_data = self.cleaned_data['input_data'].split('\n')
            for i in range(len(input_data)):
                keyword = input_data[i].split(' ')
                keyword = ' '.join(
                    list(
                        filter(
                            lambda word: not word.startswith('-'),
                            keyword
                        )
                    )
                )
                input_data[i] = keyword
            input_data = '\n'.join(input_data)
            self.cleaned_data['result'] = input_data

        return self


class UtmDeleterForm(InputForm):
    class Meta(InputForm.Meta):
        model = UtmDeleter

    def utm_delete(self):
        if self.is_valid():
            input_data = self.cleaned_data['input_data'].split('\n')
            for i in range(len(input_data)):
                input_data[i] = re.sub(r'.utm.*', '', input_data[i])
            self.cleaned_data['result'] = '\n'.join(input_data)
        return self


class ListCombinatorForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ListCombinatorForm, self).__init__(*args, **kwargs)
        self.fields['result'].required = False

    input_field = forms.Textarea()

