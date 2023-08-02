from django.contrib.auth import get_user_model
from rest_framework import status
import pytest
from model_bakery import baker
from tracker.models import Bill, Currency, Member


@pytest.fixture
def create_bill(api_client):
    def do_create_bill(bill):
        return api_client.post('/tracker/bills/', bill)
    return do_create_bill


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


@pytest.mark.django_db
class TestCreateBillItem:
    def test_if_bill_does_not_exist_returns_400(self, authenticate):
        pass
