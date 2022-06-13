# Audible series checker
Scan your audible library for book series and find the books you don't yet own

## Requirements
- python 3.10+ (may work with anything above 3.6 but i havnt tested it)
- linux (should work on other platforms but i havn't tested it)

## Install (linux)
```bash
git clone github.com/indeedhat/audible-series
cd audible-series
python -m 'venv' .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python .
```

Follow the printed instructions for logging in, your new books will written to new_books.json

## Credit
This script makes use of [https://github.com/mkb79/Audible](https://github.com/mkb79/Audible) all credit goes to them
