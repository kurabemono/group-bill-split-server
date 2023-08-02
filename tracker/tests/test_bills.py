from django.contrib.auth import get_user_model
from rest_framework import status
import pytest
from model_bakery import baker
from tracker.models import Bill, Currency, Member
from pprint import pprint


@pytest.fixture
def create_bill(api_client):
    def do_create_bill(bill):
        return api_client.post('/tracker/bills/', bill)
    return do_create_bill


@pytest.fixture
def create_billitem(api_client):
    def do_create_billitem(bill_id, billitem):
        return api_client.post(f'/tracker/bills/{bill_id}/items/', billitem)
    return do_create_billitem


@pytest.mark.django_db
class TestCreateBill:
    def test_if_user_is_anonymous_returns_401(self, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)

        response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, authenticate, create_bill):
        authenticate()
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)

        response = create_bill({
            'title': '',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_bill):
        authenticate()
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        print(currency.pk)

        response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestCreateBillItem:
    def test_if_user_is_anonymous_returns_401(self, create_billitem):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        bill = baker.make(Bill, creator=user.member)

        response = create_billitem(bill.id, {
            'name': 'test',
            'price': 1,
            'currency': currency.pk,
            'paid_date': '2023-08-01',
            'payer': user.member
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_bill_does_not_exist_returns_400(self, authenticate, create_billitem):
        authenticate()
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)

        response = create_billitem(1, {
            'name': 'test',
            'price': 1,
            'currency': currency.pk,
            'paid_date': '2023-08-01',
            'payer': user.member
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveBill:
    def test_if_bill_exists_returns_200(self, authenticate, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        api_client.force_authenticate(user=user)
        currency = baker.make(Currency)
        bill_response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill_response.data['id']

        response = api_client.get(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == bill_response.data['title']
