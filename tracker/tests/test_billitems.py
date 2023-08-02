from django.contrib.auth import get_user_model
from rest_framework import status
import pytest
from model_bakery import baker
from tracker.models import Bill, Currency, Member
from pprint import pprint


@pytest.fixture
def create_billitem(api_client):
    def do_create_billitem(bill_id, billitem):
        return api_client.post(f'/tracker/bills/{bill_id}/items/', billitem)
    return do_create_billitem


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

    def test_if_parent_bill_does_not_exist_returns_400(self, authenticate, create_billitem):
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
