import os
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .models import User, Department, Order
from users.models import Profile, Signature, LEVEL
from documents.settings import BASE_DIR


class TestOrders(TestCase):
    def setUp(self):
        cache.clear()
        self.fin_dep = Department.objects.create(code='FI', name='Finance')
        self.eng_dep = Department.objects.create(code='EN', name='Engineering')
        self.pur_dep = Department.objects.create(code='PU', name='Purchasing')
        self.gm_dep = Department.objects.create(code='GM', name='GM')
        self.anon_client = Client(USERNAME='anon', COMPUTERNAME='anon')
        self.user1_client = Client(USERNAME='user1', COMPUTERNAME='U1_pc')
        self.user2_client = Client(USERNAME='user2', COMPUTERNAME='U2_pc')
        self.hod1_client = Client(USERNAME='hod1', COMPUTERNAME='H1_pc')
        self.hod2_client = Client(USERNAME='hod2', COMPUTERNAME='H2_pc')
        self.pur1_client = Client(USERNAME='pur1', COMPUTERNAME='P2_pc')
        self.pur2_client = Client(USERNAME='pur2', COMPUTERNAME='P2_pc')
        self.fin1_client = Client(USERNAME='fin1', COMPUTERNAME='F1_pc')
        self.fin2_client = Client(USERNAME='fin2', COMPUTERNAME='F2_pc')
        self.gm_client = Client(USERNAME='GM', COMPUTERNAME='GM_pc')
        self.user1 = User.objects.create_user(
            username='user1',
            password='TestUser1',
            first_name='Ivan',
            last_name='Ivanov'
            )
        self.user1.profile.department = self.fin_dep
        self.user1.profile.save()
        self.user2 = User.objects.create_user(
            username='user2',
            password='TestUser2',
            first_name='Oleg',
            last_name='Frolov'
            )
        self.user2.profile.department = self.eng_dep
        self.user2.profile.save()
        self.hod1 = User.objects.create_user(
            username='hod1',
            password='TestHOD1',
            first_name='Irina',
            last_name='Vasina'
            )
        self.hod1.profile.sign_as = '0'
        self.hod1.profile.department = self.fin_dep
        self.hod1.profile.save()
        self.hod2 = User.objects.create_user(
            username='hod2',
            password='TestHOD2',
            first_name='Vera',
            last_name='Ivanova'
            )
        self.hod2.profile.sign_as = '0'
        self.hod2.profile.department = self.eng_dep
        self.hod2.profile.save()
        self.pur1 = User.objects.create_user(
            username='pur1',
            password='TestPUR',
            first_name='Victor',
            last_name='Petrov'
            )
        self.pur1.profile.sign_as = '1'
        self.pur1.profile.department = self.pur_dep
        self.pur1.profile.save()
        self.pur2 = User.objects.create_user(
            username='pur2',
            password='TestPUR',
            first_name='Julia',
            last_name='Povar'
            )
        self.pur2.profile.sign_as = '1'
        self.pur2.profile.department = self.pur_dep
        self.pur2.profile.save()
        self.fin1 = User.objects.create_user(
            username='fin1',
            password='TestFIN1',
            first_name='Artem',
            last_name='Sidorov'
            )
        self.fin1.profile.sign_as = '2'
        self.fin1.profile.department = self.fin_dep
        self.fin1.profile.save()
        self.fin2 = User.objects.create_user(
            username='fin2',
            password='TestFIN2',
            first_name='Olga',
            last_name='Red'
            )
        self.fin2.profile.sign_as = '2'
        self.fin2.profile.department = self.fin_dep
        self.fin2.profile.save()
        self.gm = User.objects.create_user(
            username='gm',
            password='TestGM',
            first_name='Jan',
            last_name='GM'
            )
        self.gm.profile.sign_as = '3'
        self.gm.profile.department = self.gm_dep
        self.gm.profile.save()
        self.user1_client.force_login(self.user1)
        self.user2_client.force_login(self.user2)
        self.hod1_client.force_login(self.hod1)
        self.hod2_client.force_login(self.hod2)
        self.pur1_client.force_login(self.pur1)
        self.pur2_client.force_login(self.pur2)
        self.fin1_client.force_login(self.fin1)
        self.fin2_client.force_login(self.fin2)
        self.gm_client.force_login(self.gm)
        self.order_fin = Order.objects.create(
            text='7150000 - A4 Paper',
            supplier='Romashka',
            amount=100500,
            requested_by=self.user1,
            department=self.fin_dep,
            )
        self.order_eng = Order.objects.create(
            text='6093333 - WD-40',
            supplier='Ulybka',
            amount=9000,
            requested_by=self.user2,
            department=self.eng_dep
            )
        self.ALL_CLIENTS = [
            self.user1_client, self.user2_client,
            self.hod1_client, self.hod2_client,
            self.pur1_client, self.pur2_client,
            self.fin1_client, self.fin2_client,
            self.gm_client
            ]

    def client_list_excluding(self, to_exclude):
        return [cli for cli in self.ALL_CLIENTS if cli not in to_exclude]
    
    def order_visibility(self, client, order, destination, visibility):
        response = client.get(reverse(destination))
        if visibility:
            self.assertContains(response, order.text)
        else:
            self.assertNotContains(response, order.text)
        print(response.request)

    def check_clients(self, view, no_view, order, desination):
        for client in view:
            self.order_visibility(client, order, desination, True)
        for client in no_view:
            self.order_visibility(client, order, desination, False)

    def attempt_signature(self, client, order, resolution):
        for lvl in LEVEL:
            client.post(reverse('order_sign', args=[order.id, lvl[0], resolution]))

    def test_order_on_main(self):
        no_view = [self.user2_client, self.hod2_client]
        view = self.client_list_excluding(no_view)
        self.check_clients(view, no_view, self.order_fin, 'pending_orders')

    def test_order_in_my_orders(self):
        view = [self.user1_client, ]
        no_view = self.client_list_excluding(view)
        self.check_clients(view, no_view, self.order_fin, 'my_orders')

    def test_order_all_approve(self):
        self.assertEquals(self.order_fin.signatures.count(), 0)
        for client in self.ALL_CLIENTS:
            self.attempt_signature(client, self.order_fin, True)
        print(Signature.objects.all())
        self.assertEquals(self.order_fin.signatures.count(), 4)
        self.order_fin.refresh_from_db()
        self.assertTrue(self.order_fin.all_signed)
        
    def test_order_all_decline(self):
        self.assertEquals(self.order_eng.signatures.count(), 0)
        for client in self.ALL_CLIENTS:
            self.attempt_signature(client, self.order_eng, False)
        self.assertEquals(self.order_eng.signatures.count(), 1)
        self.order_eng.refresh_from_db()
        self.assertTrue(self.order_eng.declined)

    def test_order_hod_approve_pur_decline(self):
        self.assertEquals(self.order_eng.signatures.count(), 0)
        self.attempt_signature(self.hod2_client, self.order_eng, True)
        self.assertEquals(self.order_eng.signatures.count(), 1)
        self.assertTrue(self.order_eng.signatures.filter(level='HOD').first().approved)
        self.attempt_signature(self.pur1_client, self.order_eng, False)
        self.assertEquals(self.order_eng.signatures.count(), 2)
        self.assertFalse(self.order_eng.signatures.filter(level='PUR').first().approved)
        self.order_eng.refresh_from_db()
        self.assertTrue(self.order_eng.declined)
        self.attempt_signature(self.fin1_client, self.order_eng, True)
        self.assertEquals(self.order_eng.signatures.count(), 2)

        