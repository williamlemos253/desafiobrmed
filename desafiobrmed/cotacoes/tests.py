from django.test import TestCase, Client
from .models import Taxas
from .forms import FiltroForm
from .views import rates_api, get_from_db_or_api, only_work_days, home
import datetime



# Teste do banco de dados
class TaxasModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Taxas.objects.create(date=datetime.date.today(), taxa_dolar='1', taxa_real='5', taxa_iene='100',
                             taxa_euro='0.50')

    def test_date_label(self):
        date = Taxas.objects.get(id=1)
        field_label = date._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

    def test_date(self):
        date = Taxas.objects.get(id=1)
        expected_object_value = date.date
        self.assertEquals(expected_object_value, datetime.date.today())

    def test_taxa_dolar(self):
        taxa = Taxas.objects.get(id=1)
        expected_object_value = 1
        self.assertEquals(expected_object_value, taxa.taxa_dolar)


# Teste do formulário
class FiltroFormTest(TestCase):
    def test_filtro_form_date_field_label(self):
        form = FiltroForm()
        self.assertTrue(form.fields['date'].label == 'Initial Date')

    def test_filtro_form_columns_field_label(self):
        form = FiltroForm()
        self.assertTrue(form.fields['columns'].label == 'Number of columns')

    def test_filtro_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = FiltroForm(data={'date': date, 'columns': 5})
        self.assertTrue(form.is_valid())

    def test_filtro_form_invalid_future_date(self):
        date = datetime.date.today() + datetime.timedelta(days=1)
        form = FiltroForm(data={'date': date, 'columns': 5})
        self.assertFalse(form.is_valid())

    def test_filtro_form_invalid_column_number(self):
        date = datetime.date.today()
        form = FiltroForm(data={'date': date, 'columns': 6})
        self.assertFalse(form.is_valid())


# Teste do request da api
class Rates_API_Test(TestCase):
    def test_rates_api_response(self):
        response = rates_api(datetime.date.today())
        self.assertEqual(response.status_code, 200)


# Teste da persistencia da api no banco de dados
class Get_From_Db_or_Api_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Taxas.objects.create(date=datetime.date.today(), taxa_dolar='1', taxa_real='5', taxa_iene='100',
                             taxa_euro='0.50')

    def test_get_from_db_or_api_response(self):
        date = Taxas.objects.get(id=1)
        aux = get_from_db_or_api(date.date)

        self.assertEquals(date, aux)


# Teste da função de remover dias não úteis
class Only_Work_Days_Function_Test(TestCase):

    def test_work_days(self):
        date = datetime.date(2021,12,3) #its friday
        aux = only_work_days(date)
        self.assertEquals(date, aux)

    def test_nonwork_days(self):
        date = datetime.date(2021,12,4) #its saturday
        aux = only_work_days(date)
        self.assertNotEquals(date, aux)

    def test_nonwork_days_return(self):
        date = datetime.date(2021,12,4) #its saturday
        aux = only_work_days(date)
        self.assertEquals(datetime.date(2021,12,3), aux)


# Teste da view home, não testar sem rodar python manage.py collectstatic
class HomeViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_response_at_home_view(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 200)

    def test_post_html_at_home_view(self):
        response = self.client.post('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_response_at_home_view(self):
        data = {
        'date': '2020-01-31',
        'columns': '1'
        }
        response = self.client.post('/', data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


