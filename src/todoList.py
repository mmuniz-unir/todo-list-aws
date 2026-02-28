import os
import unittest
import json
import requests
import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_listtodos(self):
        print('---------------------------------------')
        print('Starting - integration test List TODO')
        
        # Add TODO
        url = BASE_URL + "/todos"
        data = {"text": "Integration text example"}
        response = requests.post(url, data=json.dumps(data))
        jsonbody = response.json()
        ID_TODO = jsonbody['id']
        print('Created To-Do:', jsonbody)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(jsonbody['text'], "Integration text example")
        
        # List
        response = requests.get(url)
        print('Response List Todo:', response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

        # Cleanup
        requests.delete(url + '/' + ID_TODO)
        print('End - integration test List TODO')

    def test_api_addtodo(self):
        print('---------------------------------------')
        print('Starting - integration test Add TODO')
        url = BASE_URL + "/todos"
        data = {"text": "Integration text example"}
        response = requests.post(url, data=json.dumps(data))
        jsonbody = response.json()
        ID_TODO = jsonbody['id']
        print('Created To-Do:', jsonbody)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(jsonbody['text'], "Integration text example")
        
        # Delete
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(response.status_code, 200)
        print('End - integration test Add TODO')

    def test_api_gettodo(self):
        print('---------------------------------------')
        print('Starting - integration test Get TODO')
        url = BASE_URL + "/todos"
        data = {"text": "Integration text example - GET"}
        response = requests.post(url, data=json.dumps(data))
        jsonbody = response.json()
        ID_TODO = jsonbody['id']
        print('Created To-Do:', jsonbody)
        
        # Get
        response = requests.get(url + '/' + ID_TODO)
        jsonbody = response.json()
        print('Response Get Todo:', jsonbody)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(jsonbody['text'], "Integration text example - GET")

        # Delete
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(response.status_code, 200)
        print('End - integration test Get TODO')

    def test_api_updatetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Update TODO')
        url = BASE_URL + "/todos"
        data = {"text": "Integration text example - Initial"}
        response = requests.post(url, data=json.dumps(data))
        jsonbody = response.json()
        ID_TODO = jsonbody['id']
        print('Created To-Do:', jsonbody)
        
        # Update
        update_data = {"text": "Integration text example - Modified", "checked": True}
        response = requests.put(url + '/' + ID_TODO, data=json.dumps(update_data))
        jsonbody = response.json()
        print('Updated To-Do:', jsonbody)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(jsonbody['text'], "Integration text example - Modified")
        
        # Get and validate
        response = requests.get(url + '/' + ID_TODO)
        jsonbody = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(jsonbody['text'], "Integration text example - Modified")
        
        # Delete
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(response.status_code, 200)
        print('End - integration test Update TODO')

    def test_api_deletetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Delete TODO')
        url = BASE_URL + "/todos"
        data = {"text": "Integration text example - Initial"}
        response = requests.post(url, data=json.dumps(data))
        jsonbody = response.json()
        ID_TODO = jsonbody['id']
        print('Created To-Do:', jsonbody)
        
        # Delete
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(response.status_code, 200)
        print('Deleted To-Do:', ID_TODO)
        
        # Confirm deletion
        response = requests.get(url + '/' + ID_TODO)
        self.assertEqual(response.status_code, 404)
        print('End - integration test Delete TODO')