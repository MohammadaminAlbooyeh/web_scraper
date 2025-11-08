# Integration tests and recording vcrpy cassettes

This directory contains offline integration tests that either use static HTML
fixtures (under `tests/fixtures/`) or HTTP recordings (vcrpy cassettes).

Why record cassettes?
- Recording real HTTP responses with vcrpy allows you to run realistic end-to-end
  tests without hitting the network every time.
- Use cassettes to capture the site state you want to test against and keep the
  test suite stable.

How to record a new cassette with vcrpy
1. Install the development requirements (see project `requirements.txt`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run a small script to perform the requests and save a cassette. Example
   script using `requests` and `vcrpy`:

```python
import vcr
import requests

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)

with my_vcr.use_cassette('books_listing.yaml'):
    r = requests.get('http://books.toscrape.com/')
    print(r.status_code)

with my_vcr.use_cassette('sample_product.yaml'):
    r = requests.get('http://books.toscrape.com/catalogue/sample-book_1/index.html')
    print(r.status_code)
```

3. The first time you run the script it will perform real HTTP requests and
   write cassette YAML files to `tests/fixtures/cassettes/`.

4. Add cassettes to the repository (they are plain YAML) and use them in tests
   by instructing the HTTP client to use the cassette (see vcrpy docs).

Tips and best practices
- Prefer static HTML fixtures for small, deterministic unit-style integration
  tests (these are already present in `tests/fixtures/*.html`).
- Use vcrpy cassettes for higher-fidelity integration tests that exercise
  network behaviors (redirects, headers, etc.).
- Record cassettes with `record_mode='once'` to avoid accidental rewrites.
- If a site blocks automated requests, use a browser to fetch the page and save
  the HTML into `tests/fixtures/` instead of recording.

Running integration tests

- To run the offline integration tests that use static HTML fixtures:

```bash
pytest tests/integration/test_integration_offline.py -q
```

- To run tests that rely on vcrpy cassettes, ensure the cassettes exist under
  `tests/fixtures/cassettes/` and then run pytest as usual.

References
- vcrpy: https://vcrpy.readthedocs.io/
