import pytest
from fastapi.testclient import TestClient
from pytest_httpserver import HTTPServer
import pdfplumber
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import asyncio
from common_code.config import get_settings
from common_code.common.enums import FieldDescriptionType
from main import app

# Fixture to create a test PDF with skewed images


@pytest.fixture(name="test_pdf")
def test_pdf_fixture():
    """Create a test PDF with two skewed images on the first page."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Create and add a skewed image (10 degrees)
    img = Image.new('RGB', (200, 200), color='red')
    img = img.rotate(10, expand=True)  # Simulate a 10-degree skew
    img.save('temp_skewed.png')
    c.drawImage('temp_skewed.png', 100, 600, 200, 200)
    c.drawString(100, 750, "Page 1 - Image 1 (10° skew)")

    # Create and add a second skewed image (-5 degrees) on the same page
    img = Image.new('RGB', (200, 200), color='blue')
    img = img.rotate(-5, expand=True)  # Simulate a -5-degree skew
    img.save('temp_skewed2.png')
    c.drawImage('temp_skewed2.png', 100, 400, 200, 200)
    c.drawString(100, 450, "Page 1 - Image 2 (-5° skew)")

    c.showPage()
    c.save()
    buffer.seek(0)

    # Clean up temporary files
    os.remove('temp_skewed.png')
    os.remove('temp_skewed2.png')

    return buffer

# Fixture for the FastAPI test client with engine override


@pytest.fixture(name="client")
def client_fixture(reachable_engine_instance: HTTPServer):
    def get_settings_override():
        settings = get_settings()
        settings.engine_urls = [reachable_engine_instance.url_for("")]
        settings.engine_announce_retries = 2
        settings.engine_announce_retry_delay = 1
        settings.max_tasks = 2
        return settings

    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

# Fixture for a reachable engine instance


@pytest.fixture(name="reachable_engine_instance")
def reachable_engine_instance_fixture(httpserver: HTTPServer):
    httpserver.expect_request("/services").respond_with_json({}, status=200)
    yield httpserver
    httpserver.clear()

# Test successful task submission and status retrieval


@pytest.mark.asyncio
async def test_task_success(client: TestClient, test_pdf: BytesIO):
    """Test submitting a PDF correction task and checking its status."""
    # Submit a task with a valid PDF
    response = client.post("/compute", files={"pdf": ("test.pdf", test_pdf.getvalue(), "application/pdf")})
    assert response.status_code == 200
    task_data = response.json()
    assert "task_id" in task_data, "Task ID not returned in response"

    task_id = task_data["task_id"]

    # Check task status until completion
    status_response = client.get(f"/tasks/{task_id}/status")
    assert status_response.status_code == 200
    status_data = status_response.json()

    max_retries = 10
    retries = 0
    while status_data.get("status") == "RUNNING" and retries < max_retries:
        await asyncio.sleep(1)
        status_response = client.get(f"/tasks/{task_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        retries += 1

    assert status_data.get("status") == "COMPLETED", f"Task did not complete: {status_data}"
    assert "result" in status_data, "Task result not returned"
    assert status_data["result"]["corrected_pdf"]["type"] == FieldDescriptionType.APPLICATION_PDF

    # Verify the corrected PDF (basic check)
    corrected_pdf = BytesIO(status_data["result"]["corrected_pdf"]["data"])
    with pdfplumber.open(corrected_pdf) as pdf:
        assert len(pdf.pages) > 0, "Corrected PDF is empty"

# Test task status for a non-existent task


# def test_task_status_not_found(client: TestClient):
#     """Test retrieving status for a non-existent task."""
#     task_status_response = client.get("/tasks/00000000-0000-0000-0000-000000000000/status")
#     assert task_status_response.status_code == 404
#     assert "Task not found" in task_status_response.text

# Test task submission when the queue is full


@pytest.mark.asyncio
async def test_compute_queue_full(client: TestClient, test_pdf: BytesIO):
    """Test submitting tasks beyond the queue limit."""
    # Submit tasks to fill the queue (max_tasks = 2)
    response1 = client.post("/compute", files={"pdf": ("test.pdf", test_pdf.getvalue(), "application/pdf")})
    assert response1.status_code == 200
    response2 = client.post("/compute", files={"pdf": ("test.pdf", test_pdf.getvalue(), "application/pdf")})
    assert response2.status_code == 200

    # Submit a third task (should exceed queue limit)
    response3 = client.post("/compute", files={"pdf": ("test.pdf", test_pdf.getvalue(), "application/pdf")})
    assert response3.status_code == 503
    assert "Service Unavailable" in response3.text

# Test task submission with invalid input


def test_task_invalid_input(client: TestClient):
    """Test submitting a task with invalid input (non-PDF file)."""
    invalid_file = BytesIO(b"not a pdf")
    response = client.post("/compute", files={"pdf": ("invalid.txt", invalid_file.getvalue(), "text/plain")})
    assert response.status_code == 400
    assert "Invalid request" in response.text
