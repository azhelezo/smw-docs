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
            last_name='Dulin'
            )
        self.user1.profile.department = self.fin_dep
        self.user1.profile.save()
        self.user2 = User.objects.create_user(
            username='user2',
            password='TestUser2',
            first_name='Oleg',
            last_name='Ololo'
            )
        self.user2.profile.department = self.eng_dep
        self.user2.profile.save()
        self.hod1 = User.objects.create_user(
            username='hod1',
            password='TestHOD1',
            first_name='Irina',
            last_name='Nomnom'
            )
        self.hod1.profile.is_hod = True
        self.hod1.profile.department = self.fin_dep
        self.hod1.profile.save()
        self.hod2 = User.objects.create_user(
            username='hod2',
            password='TestHOD2',
            first_name='Vera',
            last_name='Ivanova'
            )
        self.hod2.profile.is_hod = True
        self.hod2.profile.department = self.eng_dep
        self.hod2.profile.save()
        self.pur1 = User.objects.create_user(
            username='pur1',
            password='TestPUR',
            first_name='Victor',
            last_name='Petrov'
            )
        self.pur1.profile.is_pur = True
        self.pur1.profile.department = self.pur_dep
        self.pur1.profile.save()
        self.pur2 = User.objects.create_user(
            username='pur2',
            password='TestPUR',
            first_name='Julia',
            last_name='Povar'
            )
        self.pur2.profile.is_pur = True
        self.pur2.profile.department = self.pur_dep
        self.pur2.profile.save()
        self.fin1 = User.objects.create_user(
            username='fin1',
            password='TestFIN1',
            first_name='Artem',
            last_name='Sidorov'
            )
        self.fin1.profile.is_pur = True
        self.fin1.profile.department = self.fin_dep
        self.fin1.profile.save()
        self.fin2 = User.objects.create_user(
            username='fin2',
            password='TestFIN2',
            first_name='Olga',
            last_name='Red'
            )
        self.fin2.profile.is_pur = True
        self.fin2.profile.department = self.fin_dep
        self.fin2.profile.save()
        self.gm = User.objects.create_user(
            username='gm',
            password='TestGM',
            first_name='Jan',
            last_name='GM'
            )
        self.gm.profile.is_pur = True
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
                supplier='Romashka',
                text='7150000 - A4 Paper',
                department=self.fin_dep,
                amount=100500,
                requested_by=self.user1
            )

    def order_visible(self, client, lookup):
        response = client.get(reverse('pending_orders'))
        self.assertContains(response, lookup)
    
    def order_not_visible(self, client, lookup):
        response = client.get(reverse('pending_orders'))
        self.assertNotContains(response, lookup)

    def attempt_signature(self, client, order):
        for lvl in LEVEL:
            response = client.post(reverse('order_sign', args=[order.id, lvl[0], True]))
            print(f'{response.wsgi_request.user} signing as {lvl[0]}')
            #print(f'{order.signatures.all().filter(level=lvl, user=response.wsgi_request.user)}')

    def test_order_visibility(self):
        view = [
            self.user1_client, self.hod1_client,
            self.pur1_client, self.pur2_client,
            self.fin1_client, self.fin2_client,
            self.gm_client
            ] #  users can see order_fin
        no_view = [self.user2_client, self.hod2_client] # users can not see order_fin

        for client in view:
            self.order_visible(client, self.order_fin.text)

        for client in no_view:
            self.order_not_visible(client, self.order_fin.text)

    def test_order_signature(self):
        clients = [
            self.user1_client, self.user2_client,
            self.hod1_client, self.hod2_client,
            self.pur1_client, self.pur2_client,
            self.fin1_client, self.fin2_client,
            self.gm_client
            ]
        for client in clients:
            self.attempt_signature(client, self.order_fin)
        print(Signature.objects.all())
        