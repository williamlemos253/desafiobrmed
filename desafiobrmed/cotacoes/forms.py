import datetime
from django import forms


VIEW_CHOICES = (
    (5, "5"),
    (4, "4"),
    (3, "3"),
    (2, "2"),
    (1, "1"),
)

class FiltroForm(forms.Form):
    date = forms.DateField(required=False, label='Initial Date')
    columns = forms.ChoiceField(choices=VIEW_CHOICES, label='Number of columns to see')

    def clean_date(self):
        date = self.cleaned_data['date']
        if not date:
            date = datetime.date.today()
        if date > datetime.date.today():
            raise forms.ValidationError("the date entered is later than today's ")
        elif date.weekday() in (5,6):
            raise forms.ValidationError("only working days are accepted")

        return date


    def clean_columns(self):
        columns = int(self.cleaned_data['columns'])
        if columns < 1 or columns > 5:
            raise forms.ValidationError("Amiguinho não tenta editar o html da página")
        return columns
