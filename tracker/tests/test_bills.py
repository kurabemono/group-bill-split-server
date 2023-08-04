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

    def test_if_data_is_valid_returns_201(self, authenticate, create_bill):
        authenticate()
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)

        response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveBill:
    def test_list_if_user_is_anonymous_returns_401(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill_response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        api_client.force_authenticate(user=None)

        response = api_client.get('/tracker/bills/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_object_if_user_is_anonymous_returns_401(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill_response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill_response.data['id']
        api_client.force_authenticate(user=None)

        response = api_client.get(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_bill_does_not_exist_returns_404(self, api_client):
        User = get_user_model()
        user = baker.make(User)
        api_client.force_authenticate(user=user)

        response = api_client.get(f'/tracker/bills/1/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_not_owner_of_bill_returns_404(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        user2 = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill_response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill_response.data['id']
        api_client.force_authenticate(user=user2)

        response = api_client.get(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_bill_exists_returns_200(self, api_client, create_bill):
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

    def test_if_member_of_bill_returns_200(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        user2 = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill_response = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk,
            'members': [user2.member.pk]
        })
        bill_id = bill_response.data['id']

        api_client.force_authenticate(user=user2)

        response = api_client.get(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == bill_response.data['title']


@pytest.mark.django_db
class TestUpdateBill:
    def test_if_put_user_is_anonymous_returns_401(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']
        api_client.force_authenticate(user=None)

        response = api_client.put(f'/tracker/bills/{bill_id}/', {
            'title': 'b',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_patch_user_is_anonymous_returns_401(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']
        api_client.force_authenticate(user=None)

        response = api_client.patch(f'/tracker/bills/{bill_id}/', {
            'title': 'b',
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_creator_returns_403(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        user2 = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']
        api_client.force_authenticate(user=user2)

        response = api_client.put(f'/tracker/bills/{bill_id}/', {
            'title': 'b',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']

        response = api_client.patch(f'/tracker/bills/{bill_id}/', {
            'title': '',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']

        response = api_client.patch(f'/tracker/bills/{bill_id}/', {
            'title': 'b',
        })

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteBill:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']
        api_client.force_authenticate(user=None)

        response = api_client.delete(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_creator_returns_403(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        user2 = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']
        api_client.force_authenticate(user=user2)

        response = api_client.delete(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_creator_returns_204(self, api_client, create_bill):
        User = get_user_model()
        user = baker.make(User)
        user2 = baker.make(User)
        currency = baker.make(Currency)
        api_client.force_authenticate(user=user)
        bill = create_bill({
            'title': 'a',
            'display_currency': currency.pk,
            'creator': user.member.pk
        })
        bill_id = bill.data['id']

        response = api_client.delete(f'/tracker/bills/{bill_id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
