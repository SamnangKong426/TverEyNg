import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

client = TestClient(app)


# 1. Test CREATE a camera
def test_create_camera():
    payload = {"name": "Front Door", "ip": "192.168.1.50", "user_id": 1}
    response = client.post("/camera/", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


# 2. Test GET all cameras
def test_read_cameras():
    response = client.get("/camera/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 3. Test UPDATE a camera
def test_update_camera():
    camera_id = 6
    update_payload = {"name": "Updated Door", "ip": "192.168.1.99"}
    response = client.put(f"/camera/{camera_id}", json=update_payload)

    if response.status_code == 200:
        assert response.json()["status"] == "updated"
    else:
        assert response.status_code == 404


# 4. Test DELETE a camera
def test_delete_camera():
    camera_id = 1
    response = client.delete(f"/camera/{camera_id}")
    assert response.status_code in [200, 404]
