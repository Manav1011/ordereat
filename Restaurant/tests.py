from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Franchise, Outlet, MenuCategory, MenuItem
from django.core.files.uploadedfile import SimpleUploadedFile

class FranchiseAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.get(
            email='manavshah1011.ms@gmail.com', password='Manav@1011'
        )        
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        self.franchise_url = reverse('franchise-list-create')

    def test_create_franchise(self):
        data = {'name': 'Test Franchise', 'slug': 'test-franchise'}
        response = self.client.post(self.franchise_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Franchise.objects.count(), 1)

    def test_list_franchises(self):
        Franchise.objects.create(name='Test Franchise', slug='test-franchise')
        response = self.client.get(self.franchise_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class OutletAPITestCase(APITestCase):
    def setUp(self):
        self.restaurant_admin = get_user_model().objects.get(
            email = '196330307556.manav.shah@gmail.com', password='Manav@1011'
        )
        self.franchise = Franchise.objects.create(name='Test Franchise', slug='test-franchise')
        self.franchise.admin = self.superuser
        self.franchise.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.restaurant_admin)
        self.outlet_url = reverse('outlet-list-create')

    def test_create_outlet(self):
        data = {'name': 'Test Outlet', 'slug': 'test-outlet', 'franchise': self.franchise.id}
        response = self.client.post(self.outlet_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Outlet.objects.count(), 1)

    def test_list_outlets(self):
        Outlet.objects.create(name='Test Outlet', slug='test-outlet', franchise=self.franchise)
        response = self.client.get(self.outlet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class MenuCategoryAPITestCase(APITestCase):
    def setUp(self):
        self.outlet_admin =get_user_model().objects.get(
            email='22csman033@ldce.ac.in', password='Manav@1011'
        )
        self.franchise = Franchise.objects.create(name='Test Franchise', slug='test-franchise')
        self.franchise.admin = self.superuser
        self.franchise.save()
        self.outlet = Outlet.objects.create(name='Test Outlet', slug='test-outlet', franchise=self.franchise, admin=self.superuser)
        self.client = APIClient()
        self.client.force_authenticate(user=self.outlet_admin)
        self.category_url = reverse('menucategory-list-create')

    def test_create_category(self):
        data = {'name': 'Starters', 'slug': 'starters', 'outlet': self.outlet.id}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuCategory.objects.count(), 1)

    def test_list_categories(self):
        MenuCategory.objects.create(name='Starters', slug='starters', outlet=self.outlet)
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class MenuItemAPITestCase(APITestCase):
    def setUp(self):
        self.outlet_admin =get_user_model().objects.get(
            email='22csman033@ldce.ac.in', password='Manav@1011'
        )
        self.franchise = Franchise.objects.create(name='Test Franchise', slug='test-franchise')
        self.franchise.admin = self.superuser
        self.franchise.save()
        self.outlet = Outlet.objects.create(name='Test Outlet', slug='test-outlet', franchise=self.franchise, admin=self.superuser)
        self.category = MenuCategory.objects.create(name='Starters', slug='starters', outlet=self.outlet)
        self.client = APIClient()
        self.client.force_authenticate(user=self.outlet_admin)
        self.menuitem_url = reverse('menuitem-list-create')

    def test_create_menuitem(self):
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'name': 'Spring Roll',
            'slug': 'spring-roll',
            'category': self.category.id,
            'description': 'Crispy rolls',
            'price': 100,
            'image': image
        }
        response = self.client.post(self.menuitem_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 1)

    def test_list_menuitems(self):
        MenuItem.objects.create(
            name='Spring Roll', slug='spring-roll', category=self.category,
            description='Crispy rolls', price=100
        )
        response = self.client.get(self.menuitem_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
