import datetime
import requests
from django.shortcuts import render
from .forms import FiltroForm
from .models import Taxas


# Consulta api do vat
def rates_api(date):
    response = requests.get('https://api.vatcomply.com/rates?base=USD&date=' + str(date))
    return response

# Verifica se já existe no banco de dados ou chama a função de consulta da api
def get_from_db_or_api(date):
    taxes = Taxas.objects.filter(date=date)

    if taxes.exists():
        pass
    else:
        aux_rates = rates_api(date).json()
        aux_rates = Taxas(date=date, taxa_dolar=aux_rates['rates']['USD'], \
                          taxa_real=aux_rates['rates']['BRL'], \
                          taxa_iene=aux_rates['rates']['JPY'], taxa_euro=aux_rates['rates']['EUR'])
        aux_rates.save()

    aux_rates = taxes.get()
    return aux_rates


# view
def home(request, date=datetime.date.today(), columns=5):
    count = 0
    taxes=[]
    form = FiltroForm()

    if request.method == "POST":
        form = FiltroForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            columns = form.cleaned_data.get('columns')

    while count < columns:
        taxe = get_from_db_or_api(date)
        taxes.insert(0,taxe)
        count +=1
        date = taxe.date - datetime.timedelta(days=1)

    return render(request, 'home.html', {'taxes': taxes, 'form':form})
