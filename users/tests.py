from django.urls import reverse
from django.test import Client, TestCase


class TestIndex(TestCase):
    def test_index_opens(self):
        c = Client()
        response = self.c.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_index_context(self):
        c = Client()
        response = self.c.get(reverse('home'))
        self.assertEqual(response.context, {})


class TestAccount(TestCase):
    def test_account_opens(self):
        c = Client()
        response = self.c.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_account_context(self):
        c = Client()
        response = self.c.get(reverse('account'))
        self.assertEqual(response.context, {})


class TestShoppingCart(TestCase):
    def test_shoppingcart_opens(self):
        c = Client()
        response = self.c.get(reverse('shopping_cart'))
        self.assertEqual(response.status_code, 200)

    def test_shoppingcart_context(self):
        c = Client()
        response = self.c.get(reverse('shopping_cart'))
        self.assertEqual(response.context, {})


class TestRoom(TestCase):
    def test_room_opens(self):
        c = Client()
        response = self.c.get(reverse('room'))
        self.assertEqual(response.status_code, 200)

    def test_room_context(self):
        c = Client()
        response = self.c.get(reverse('room'))
        self.assertEqual(response.context, {})


