import unittest

from models.Contact import Contact


class ContactApiTest(unittest.TestCase):
    def setUp(self):
        from app import app

        # get the flask app in test mode
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_contacts_list(self):
        response = self.app.get("/contacts")
        self.assertEqual(response.status_code, 200)

    def test_contacts_get_unknown_id_aborts(self):
        response = self.app.get("/contacts/xxxxx")
        self.assertEqual(response.status_code, 404)

    def test_contacts_delete_unknown_id_aborts(self):
        response = self.app.delete("/contacts/xxxxx")
        self.assertEqual(response.status_code, 404)

    def test_contacts_post(self):
        response = self.app.post(
            "/contacts", json={"name": "test", "email": "test@example.com"})
        data = response.get_json()
        contact = Contact(**data)
        self.assertEqual(contact.name, "test")
        self.assertEqual(contact.email, "test@example.com")
        # since at that point id is not None, the contact has been created in db.
        self.assertIsNotNone(contact.id)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
