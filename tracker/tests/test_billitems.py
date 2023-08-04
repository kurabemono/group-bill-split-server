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
    def test_if_user_is_anonymous_returns_401(self, api_client, create_billitem):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        bill = baker.make(Bill, creator=user.member)
        api_client.force_authenticate(user=None)

        response = create_billitem(bill.pk, {
            'name': 'test',
            'price': 1,
            'currency': currency.pk,
            'paid_date': '2023-08-01',
            'creator': user.member.pk
        })
        pprint(response.data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_parent_bill_does_not_exist_returns_403(self, api_client, create_billitem):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user)

        response = create_billitem(1, {
            'name': 'test',
            'price': 1,
            'currency': currency.pk,
            'paid_date': '2023-08-01',
            'creator': user.member.pk
        })
        pprint(response.data['detail'])

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_bill_owner_returns_403(self, api_client, create_billitem):
        User = get_user_model()
        user = baker.make(User)
        user2 = baker.make(User)
        currency = baker.make(Currency)
        bill = baker.make(Bill, creator=user.member)
        api_client.force_authenticate(user=user2)

        response = create_billitem(bill.pk, {
            'name': 'test',
            'price': 1,
            'currency': currency.pk,
            'paid_date': '2023-08-01',
            'creator': user2.member.pk
        })
        pprint(response.data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_not_bill_member_returns_404(self):
        pass
