import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

client = TestClient(app)


def test_upload_image():
    file_path = "assets/image.jpg"
    
    with open(file_path, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        response = client.post("/alert", files=files)
        
    assert response.status_code == 200
