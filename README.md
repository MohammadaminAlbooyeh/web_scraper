# Web Scraper Project

A robust web scraper built with Scrapy for extracting book information from books.toscrape.com. Features data validation, multiple storage backends, and comprehensive testing.

## Features

- Scrapes detailed book information including title, price, availability, and more
- Data validation using Pydantic
- Multiple storage backends (JSON Lines and SQLite)
- Configurable scraping settings (rate limiting, retries, user agents)
- Comprehensive test suite
- Docker support

## Installation

### Using Docker

```bash
# Build the image
docker build -t web_scraper .

# Run the scraper
docker run web_scraper
```

### Local Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

## Usage

```bash
# Run the spider
make run

# Run tests
pytest

# Run linting
pre-commit run --all-files
```

## Data Validation

This project uses Pydantic for comprehensive data validation. Below are the validation rules for scraped book data:

### Basic Information
- **Title**
  - Required field
  - Must be a non-empty string

- **Price**
  - Required field
  - Must be a non-negative decimal number
  - Supports string inputs that can be converted to decimals

- **Description**
  - Optional field
  - Free-form text

### Book-Specific Details
- **ISBN**
  - Optional field
  - When provided:
    - Must be exactly 10 or 13 digits
    - Hyphens and spaces are automatically removed
    - Must contain only digits after cleaning

- **UPC**
  - Required field
  - Must be a non-empty string

- **Product Type**
  - Required field
  - Must be a non-empty string

### Pricing Details
- **Price (Excluding Tax)**
  - Required field
  - Must be a non-negative decimal
  - Supports string inputs (automatically converted)

- **Price (Including Tax)**
  - Required field
  - Must be a non-negative decimal
  - Must equal price_excl_tax + tax (within £0.01 rounding tolerance)

- **Tax**
  - Required field
  - Must be a non-negative decimal

### Inventory Information
- **Availability**
  - Required field
  - Must be a non-negative integer
  - String inputs are automatically converted

- **Number of Reviews**
  - Required field
  - Must be a non-negative integer

### Categories and Rating
- **Category**
  - Optional field
  - String type

- **Star Rating**
  - Required field
  - Integer between 1 and 5 (inclusive)

### URLs and Meta Information
- **Image URL**
  - Required field
  - Must be a valid HTTP/HTTPS URL
  - Automatically validated URL format

- **Product URL**
  - Required field
  - Must be a valid HTTP/HTTPS URL

- **Scrape Date**
  - Required field
  - Must be a valid datetime
  - Cannot be in the future
  - Supports ISO format string inputs

### Example Valid Item

```python
{
    "title": "Sample Book",
    "price": "9.99",
    "description": "A great book about testing",
    "isbn": "1234567890",  # or "1234567890123" for ISBN-13
    "upc": "A123456789",
    "product_type": "Books",
    "price_excl_tax": "8.99",
    "price_incl_tax": "9.99",
    "tax": "1.00",
    "availability": 5,
    "number_of_reviews": 10,
    "category": "Fiction",
    "star_rating": 4,
    "image_url": "https://example.com/image.jpg",
    "url": "https://example.com/book",
    "scrape_date": "2025-11-06T10:00:00"
}
```

### Validation in Action

The validation system:
1. Runs automatically in the pipeline
2. Converts string inputs to appropriate types
3. Validates all constraints
4. Raises detailed error messages for invalid data

Example error messages:
```python
# Invalid ISBN
ValidationError: ISBN must be 10 or 13 digits

# Invalid price
ValidationError: ensure this value is greater than or equal to 0

# Invalid star rating
ValidationError: ensure this value is less than or equal to 5

# Invalid URL
ValidationError: invalid or missing URL scheme
```

## Project Structure

```
web_scraper/
├── books/               # Compatibility shim package
├── web_scraper_project/ # Main package
│   ├── items.py        # Scrapy item definitions
│   ├── pipelines.py    # Data processing pipelines
│   ├── schemas.py      # Pydantic validation models
│   └── settings.py     # Scrapy settings
├── tests/              # Test suite
├── data/              # Output directory
├── Dockerfile         # Docker configuration
├── Makefile          # Build and run commands
├── requirements.txt   # Python dependencies
└── scrapy.cfg        # Scrapy configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests and linting
4. Submit a pull request

## License

MIT License - see LICENSE file for details
