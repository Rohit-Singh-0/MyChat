from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import json
import urllib.request
from .models import RoomMember

class AgoraSDKTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure temporary values exist during testing
        if not hasattr(settings, 'AGORA_APP_ID'):
            settings.AGORA_APP_ID = 'test_app_id'
        if not hasattr(settings, 'AGORA_APP_CERTIFICATE'):
            settings.AGORA_APP_CERTIFICATE = 'test_app_certificate'

    def test_agora_cdn_availability(self):
        """
        Verify that the new Agora SDK CDN link is active and returns HTTP 200.
        """
        cdn_url = 'https://download.agora.io/sdk/release/AgoraRTC_N-4.23.1.js'
        try:
            req = urllib.request.Request(cdn_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            self.assertEqual(response.status, 200, "CDN URL did not return 200 OK")
            content_type = response.headers.get('Content-Type', '')
            self.assertIn('application/javascript', content_type)
        except urllib.error.URLError as e:
            self.fail(f"Failed to reach SDK CDN URL: {e}")

class MyChatViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.channel_name = 'TEST_ROOM'
        self.user_name = 'TEST_USER'
        self.uid = 12345
        if not hasattr(settings, 'AGORA_APP_ID'):
            settings.AGORA_APP_ID = 'test_app_id'
        if not hasattr(settings, 'AGORA_APP_CERTIFICATE'):
            settings.AGORA_APP_CERTIFICATE = 'test_app_certificate'

    def test_get_token_view(self):
        """
        Verify /get_token/ returns valid JSON containing token, uid, and appId.
        """
        response = self.client.get('/get_token/', {'channel': self.channel_name})
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON
        data = response.json()
        self.assertIn('token', data)
        self.assertIn('uid', data)
        self.assertIn('appId', data)
        self.assertEqual(data['appId'], settings.AGORA_APP_ID)

    def test_create_and_get_member(self):
        """
        Verify that a member can be created via POST and retrieved via GET.
        """
        # Create Member
        payload = {
            'name': self.user_name,
            'UID': self.uid,
            'room_name': self.channel_name
        }
        response = self.client.post('/create_member/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], self.user_name)

        # Check DB directly
        member = RoomMember.objects.get(uid=self.uid, room_name=self.channel_name)
        self.assertEqual(member.name, self.user_name)

        # Retrieve Member
        response = self.client.get('/get_member/', {'UID': self.uid, 'room_name': self.channel_name})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], self.user_name)

    def test_delete_member(self):
        """
        Verify that a member can be deleted via POST.
        """
        RoomMember.objects.create(name=self.user_name, uid=self.uid, room_name=self.channel_name)
        
        payload = {
            'name': self.user_name,
            'UID': self.uid,
            'room_name': self.channel_name
        }
        response = self.client.post('/delete_member/', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check DB directly to ensure deletion
        with self.assertRaises(RoomMember.DoesNotExist):
            RoomMember.objects.get(uid=self.uid, room_name=self.channel_name)
