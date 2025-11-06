"""Tests for Pydantic schema validation."""

from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from pydantic import ValidationError

from web_scraper_project.schemas import ProductModel


@pytest.fixture
def valid_product_data():
    """Create a dictionary with valid product data."""
    return {
        "title": "Sample Book",
        "price": Decimal("9.99"),
        "description": "A great book about testing",
        "isbn": "1234567890",
        "upc": "A123456789",
        "product_type": "Books",
        "price_excl_tax": Decimal("8.99"),
        "price_incl_tax": Decimal("9.99"),
        "tax": Decimal("1.00"),
        "availability": 5,
        "number_of_reviews": 10,
        "category": "Fiction",
        "star_rating": 4,
        "image_url": "https://example.com/image.jpg",
        "url": "https://example.com/book",
        "scrape_date": datetime.now()
    }


class TestProductModel:
    """Test suite for ProductModel validation."""

    def test_valid_product(self, valid_product_data):
        """Test that valid data passes validation."""
        product = ProductModel(**valid_product_data)
        assert product.title == valid_product_data["title"]
        assert product.price == valid_product_data["price"]
        assert product.isbn == valid_product_data["isbn"]

    def test_required_fields(self):
        """Test that required fields raise ValidationError when missing."""
        minimal_data = {
            "title": "Test Book",
            "price": "9.99",
            "upc": "123456789",
            "product_type": "Books",
            "price_excl_tax": "8.99",
            "price_incl_tax": "9.99",
            "tax": "1.00",
            "availability": 5,
            "number_of_reviews": 10,
            "star_rating": 4,
            "image_url": "https://example.com/image.jpg",
            "url": "https://example.com/book",
            "scrape_date": datetime.now()
        }

        # Test each required field
        for field in minimal_data.keys():
            if field != "description" and field != "category" and field != "isbn":
                invalid_data = minimal_data.copy()
                del invalid_data[field]
                with pytest.raises(ValidationError) as exc_info:
                    ProductModel(**invalid_data)
                assert field in str(exc_info.value)

    def test_price_validation(self, valid_product_data):
        """Test price-related validations."""
        # Test negative prices
        for price_field in ["price", "price_excl_tax", "price_incl_tax", "tax"]:
            invalid_data = valid_product_data.copy()
            invalid_data[price_field] = Decimal("-1.00")
            with pytest.raises(ValidationError) as exc_info:
                ProductModel(**invalid_data)
            assert price_field in str(exc_info.value)
            assert "greater than or equal to 0" in str(exc_info.value)

        # Test price_incl_tax validation
        invalid_data = valid_product_data.copy()
        invalid_data["price_incl_tax"] = Decimal("20.00")  # Doesn't match excl_tax + tax
        with pytest.raises(ValidationError) as exc_info:
            ProductModel(**invalid_data)
        assert "price_incl_tax must equal price_excl_tax + tax" in str(exc_info.value)

    def test_isbn_validation(self, valid_product_data):
        """Test ISBN validation rules."""
        # Test invalid ISBN lengths
        invalid_data = valid_product_data.copy()
        invalid_data["isbn"] = "123"  # Too short
        with pytest.raises(ValidationError) as exc_info:
            ProductModel(**invalid_data)
        assert "ISBN must be 10 or 13 digits" in str(exc_info.value)

        # Test non-digit ISBN
        invalid_data["isbn"] = "123abc4567"
        with pytest.raises(ValidationError) as exc_info:
            ProductModel(**invalid_data)
        assert "ISBN must contain only digits" in str(exc_info.value)

        # Test valid ISBN-13
        valid_data = valid_product_data.copy()
        valid_data["isbn"] = "1234567890123"
        product = ProductModel(**valid_data)
        assert product.isbn == "1234567890123"

    def test_star_rating_validation(self, valid_product_data):
        """Test star rating validation."""
        # Test rating too low
        invalid_data = valid_product_data.copy()
        invalid_data["star_rating"] = 0
        with pytest.raises(ValidationError) as exc_info:
            ProductModel(**invalid_data)
        assert "greater than or equal to 1" in str(exc_info.value)

        # Test rating too high
        invalid_data["star_rating"] = 6
        with pytest.raises(ValidationError) as exc_info:
            ProductModel(**invalid_data)
        assert "less than or equal to 5" in str(exc_info.value)

    def test_url_validation(self, valid_product_data):
        """Test URL validation."""
        # Test invalid URLs
        invalid_data = valid_product_data.copy()
        for url_field in ["image_url", "url"]:
            invalid_data[url_field] = "not-a-url"
            with pytest.raises(ValidationError) as exc_info:
                ProductModel(**invalid_data)
            assert url_field in str(exc_info.value)
            assert "URL" in str(exc_info.value)

    def test_scrape_date_validation(self, valid_product_data):
        """Test scrape date validation."""
        # Test future date
        invalid_data = valid_product_data.copy()
        invalid_data["scrape_date"] = datetime.now() + timedelta(days=1)
        with pytest.raises(ValidationError) as exc_info:
            ProductModel(**invalid_data)
        assert "scrape_date cannot be in the future" in str(exc_info.value)

    def test_optional_fields(self, valid_product_data):
        """Test that optional fields can be None."""
        optional_fields = ["description", "category", "isbn"]
        for field in optional_fields:
            valid_data = valid_product_data.copy()
            valid_data[field] = None
            product = ProductModel(**valid_data)
            assert getattr(product, field) is None

    def test_type_coercion(self):
        """Test that the model properly coerces string inputs to the right types."""
        string_data = {
            "title": "Test Book",
            "price": "9.99",
            "upc": "123456789",
            "product_type": "Books",
            "price_excl_tax": "8.99",
            "price_incl_tax": "9.99",
            "tax": "1.00",
            "availability": "5",
            "number_of_reviews": "10",
            "star_rating": "4",
            "image_url": "https://example.com/image.jpg",
            "url": "https://example.com/book",
            "scrape_date": "2025-11-06T10:00:00"
        }
        
        product = ProductModel(**string_data)
        assert isinstance(product.price, Decimal)
        assert isinstance(product.availability, int)
        assert isinstance(product.scrape_date, datetime)