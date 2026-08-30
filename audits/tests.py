from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Transaction


class TransactionAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="testpass123"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="testpass123"
        )

        self.transaction1 = Transaction.objects.create(
            user=self.user1,
            transaction_type="expense",
            amount=5000,
            category="transport",
            description="Uber to office",
            transaction_date="2026-08-30"
        )

        self.transaction2 = Transaction.objects.create(
            user=self.user2,
            transaction_type="expense",
            amount=3000,
            category="food",
            description="Lunch",
            transaction_date="2026-08-30"
        )

    def test_authenticated_user_can_see_own_transactions(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/api/transactions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Uber to office")

    def test_user_cannot_see_another_users_transactions(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/api/transactions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transaction_ids = [
            transaction["id"]
            for transaction in response.data
        ]

        self.assertIn(self.transaction1.id, transaction_ids)
        self.assertNotIn(self.transaction2.id, transaction_ids)

    def test_user_can_create_transaction(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "transaction_type": "expense",
            "amount": "7000.00",
            "category": "shopping",
            "description": "New shoes",
            "transaction_date": "2026-08-30"
        }

        response = self.client.post(
            "/api/transactions/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        transaction = Transaction.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(transaction.user, self.user1)

    def test_user_cannot_update_another_users_transaction(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "transaction_type": "expense",
            "amount": "9999.00",
            "category": "shopping",
            "description": "Attempted update",
            "transaction_date": "2026-08-30"
        }

        response = self.client.put(
            f"/api/transactions/{self.transaction2.id}/",
            data,
            format="json"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND
            ]
        )

    def test_user_cannot_delete_another_users_transaction(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            f"/api/transactions/{self.transaction2.id}/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND
            ]
        )

        self.assertTrue(
            Transaction.objects.filter(
                id=self.transaction2.id
            ).exists()
        )