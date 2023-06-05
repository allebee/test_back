import pytest
from fastapi.testclient import TestClient
from PIL import Image
from io import BytesIO
from main import app

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200


def test_post_detect_weapon():
    image = Image.new("RGB", (100, 100), color="red")
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    response = client.post(
        "/detect_weapon", files={"image": ("image.png", image_bytes, "image/png")}
    )
    assert response.status_code == 200

    assert '<img src="data:image/png;base64,' in response.text


def test_post_detect_weapon_invalid_input():
    invalid_file = BytesIO(b"This is not an image")

    response = client.post(
        "/detect_weapon", files={"image": ("invalid.txt", invalid_file, "text/plain")}
    )
    assert response.status_code == 500

    assert "Error:" in response.text


if __name__ == "__main__":
    pytest.main()
