
def create_test_user(client):
    """Helper function to create a test user"""
    response = client.post("/api/admin/add_user", 
            content_type='application/json',
            json={"first_name": "test", "last_name": "test", "email": "test@test.test", "password": "test", "role": 2}
        )
    return response
