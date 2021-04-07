import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from . import forms
from . import models


class MenuModelsTests(TestCase):
    def setUp(self):
        user = User.objects.create(
            username = "orion",
            email = "test@test.com",
            password = "password"
        )
        ingredient = models.Ingredient.objects.create(
            name = "ingredient"
        )
        item = models.Item.objects.create(
            name = "item",
            description = "an item",
            chef = user,
        )
        item.ingredients.add(ingredient)
        menu = models.Menu.objects.create(
            season = "Spring 2021",
            creator = user,
            expiration_date = datetime.date.today() +
                              datetime.timedelta(days=1),
        )
        menu.items.add(item)

    def test_user_creation(self):
        """Test that a user was created"""
        user = models.User.objects.get(id=1)
        self.assertEqual(user.username, "orion")

    def test_ingredient_creation(self):
        """Test that an ingredient was created"""
        ingredient = models.Ingredient.objects.get(id=1)
        self.assertEqual(ingredient.name, "ingredient")

    def test_ingredient_str(self):
        """Test the Ingredient __str__ method"""
        ingredient = models.Ingredient.objects.get(id=1)
        self.assertEqual(ingredient.__str__(), ingredient.name)

    def test_item_creation(self):
        """Test that an Item was created"""
        item = models.Item.objects.get(id=1)
        self.assertEqual(item.name, "item")

    def test_item_str(self):
        """Test the Item __str__ method"""
        item = models.Item.objects.get(id=1)
        self.assertEqual(item.__str__(), item.name)

    def test_menu_creation(self):
        """Test that a menu was created"""
        menu = models.Menu.objects.get(id=1)
        self.assertEqual(menu.season, "Spring 2021")

    def test_menu_str(self):
        """Test the Menu __str__ method"""
        menu = models.Menu.objects.get(id=1)
        self.assertEqual(menu.__str__(), menu.season)

    def test_many_to_many_relationships(self):
        """
        Test that ingredients are added to items
        and that items are added to menus
        """
        menu = models.Menu.objects.get(id=1)
        item = models.Item.objects.get(id=1)
        self.assertEqual(menu.items.count(), 1)
        self.assertNotEqual(menu.items.count(), 0)
        self.assertEqual(item.ingredients.count(), 1)
        self.assertNotEqual(item.ingredients.count(), 0)


class MenuViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = "orion",
            email = "test@test.com",
            password = "password"
        )
        self.ingredient = models.Ingredient.objects.create(
            name = "ingredient"
        )
        self.item = models.Item.objects.create(
            name = "item",
            description = "an item",
            chef = self.user,
        )
        self.item.ingredients.add(self.ingredient)
        self.menu = models.Menu.objects.create(
            season = "Spring 2021",
            creator = self.user,
            expiration_date = datetime.date.today() +
                              datetime.timedelta(days=1),
        )
        self.menu.items.add(self.item)

    def test_sign_in_view(self):
        """Test for the sign-in view"""
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/login.html')

    def test_sign_in_post_view(self):
        """Test a POST to the sign in view"""
        resp = self.client.post(
            reverse('login'),
            {
                'username': 'orion',
                'password': 'password'
            }, follow=True
        )
        self.assertEqual(resp.status_code, 200)

    def test_register_view(self):
        """Test for the register view"""
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/register.html')

    def test_register_post_view(self):
        """Test a POST to the register view"""
        resp = self.client.post(
            reverse('register'),
            {
                'username': 'orion2',
                'email': 'test@test.com',
                'verify_email': 'test@test.com',
                'password1': 'password',
                'password2': 'password'
            }
        )
        self.assertEqual(resp.status_code, 302)

    def test_sign_out_view(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)

    def test_current_menu_list(self):
        """Test for the current menu list view"""
        resp = self.client.get(reverse('current_menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/current_menus.html')
        self.assertEqual(resp.context['menus'].count(), 1)

    def test_menu_detail_view(self):
        """Test for the menu detail view"""
        resp = self.client.get(reverse('menu_detail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_item_detail_view(self):
        """Test for the item detail view"""
        resp = self.client.get(reverse('item_detail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/item_detail.html')

    def test_create_menu_view(self):
        """Test for the create menu view"""
        self.client.force_login(self.user)
        resp = self.client.get(reverse('create_menu'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/create_menu.html')

    def test_create_menu_post_view(self):
        """Test a POST to the create menu view"""
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse('create_menu'),
            {
                'season': 'Spring',
                'year': '2021',
                'items': '1',
                'expiration_date': datetime.date.today() +
                                   datetime.timedelta(days=1),
            }, follow=True
        )
        self.assertContains(resp, "Spring 2021")

    def test_edit_menu_view(self):
        """Test for the edit menu view"""
        self.client.force_login(self.user)
        resp = self.client.get(reverse('edit_menu', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertTemplateUsed(resp, 'menu/edit_menu.html')

    def test_edit_menu_post_view(self):
        """Test a POST to the edit menu view"""
        self.client.force_login(self.user)
        resp = self.client.post(
            reverse('edit_menu', args=[1]),
            {
                'season': 'Fall',
                'year': '2021',
                'items': '1',
                'expiration_date': datetime.date.today() +
                                   datetime.timedelta(days=1),
            }, follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Fall 2021")


if __name__ == '__main__':
    unittest.main()
