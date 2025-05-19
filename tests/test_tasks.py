import pytest
from fastapi.testclient import TestClient
import pdfplumber
from io import BytesIO
import cv2
import numpy as np
from services.cv2skewpredictor import CV2SkewPredictor

# Fixture to load the test PDF from the fixtures directory


@pytest.fixture(name="test_pdf")
def test_pdf_fixture():
    """Load a test PDF with skewed images from the fixtures directory."""
    pdf_path = "tests/fixtures/test_skewed.pdf"
    try:
        with open(pdf_path, "rb") as f:
            return BytesIO(f.read())
    except FileNotFoundError:
        pytest.fail(f"Test PDF not found at {pdf_path}. Please add test_skewed.pdf to tests/fixtures/.")

# Fixture for the FastAPI test client


@pytest.fixture(name="client")
def client_fixture():
    from main import app
    with TestClient(app) as client:
        yield client


def test_process_valid_pdf(client: TestClient, test_pdf: BytesIO):
    """Test processing a valid PDF with skewed images."""
    # Send the PDF to the /compute endpoint
    response = client.post("/compute", files={"pdf": ("test.pdf", test_pdf.getvalue(), "application/pdf")})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

    # Use CV2SkewPredictor to check the orientation of images in the corrected PDF
    skew_predictor = CV2SkewPredictor()
    with pdfplumber.open(corrected_pdf) as pdf:
        for page_num, page in enumerate(pdf.pages):
            images = page.images  # Extract images from the page
            if not images:
                pytest.fail(f"No images found on page {page_num + 1} of corrected PDF")

            for img_idx, img in enumerate(images):
                # Extract raw image data and convert to OpenCV format
                img_bytes = img["stream"].get_data()  # Get raw image bytes
                img_array = np.frombuffer(img_bytes, np.uint8)
                img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img_cv is None:
                    pytest.fail(f"Failed to decode image {img_idx + 1} on page {page_num + 1}")

                # Predict the skew angle of the corrected image
                skew_angle = skew_predictor.process(img_cv)

                # Verify that the skew angle is approximately 0 (within tolerance)
                tolerance = 0.5  # Allow ±0.5 degrees
                assert abs(skew_angle) <= tolerance, (
                    f"Image {img_idx + 1} on page {page_num + 1} is not corrected: "
                    f"skew angle is {skew_angle}, expected ~0 (tolerance ±{tolerance})"
                )


def test_process_invalid_pdf(client: TestClient):
    """Test processing an invalid PDF (non-PDF file)."""
    invalid_file = BytesIO(b"not a pdf")
    response = client.post("/compute", files={"pdf": ("invalid.txt", invalid_file.getvalue(), "text/plain")})
    assert response.status_code == 400
    assert "Invalid request" in response.text


def test_process_pdf_with_multiple_images(client: TestClient, test_pdf: BytesIO):
    """Test processing a PDF with multiple images per page."""
    response = client.post("/compute", files={"pdf": ("test.pdf", test_pdf.getvalue(), "application/pdf")})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    corrected_pdf = BytesIO(response.content)
    with pdfplumber.open(corrected_pdf) as pdf:
        for page_num, page in enumerate(pdf.pages):
            images = page.images
            assert len(images) > 0, f"No images found on page {page_num + 1}"
            # Verify that all images are processed (orientation check already done in test_process_valid_pdf)
