import json
import os
import audible

LOGIN_FILE = ".login"
LIBRARY_FILE = "library.json"
NEW_BOOKS_FILE = "new_books.json"

def get_client() -> audible.Client:
    if not os.path.exists(LOGIN_FILE):
        auth = audible.Authenticator.from_login_external(locale="uk")
        auth.to_file(LOGIN_FILE)
    else:
        auth = audible.Authenticator.from_file(filename=LOGIN_FILE)

    return audible.Client(auth=auth)


def load_library_asns(client) -> list:
    if os.path.exists(LIBRARY_FILE):
        print(f"{LIBRARY_FILE} exists")
        books = json.load(open(LIBRARY_FILE))
    else:
        books = client.get("library", num_results=500)
        with open(LIBRARY_FILE, "w") as new:
            new.write(json.dumps(books, indent="    "))

    book_asns = []
    for book in books["items"]:
        book_asns.append(book["asin"])

    return book_asns


def existing_file_check():
    if os.path.exists(NEW_BOOKS_FILE):
        print(f"{NEW_BOOKS_FILE} exists!\nPlease delete it before running again")
        exit(1)


def main():
    existing_file_check()

    with get_client() as client:
        checked = []
        new_books = {}
        to_check = load_library_asns(client)

        for asin in to_check:
            if asin in checked:
                print(f"{asin} - skip")
                continue
            print(asin)

            checked.append(asin)

            books = client.get(f"catalog/products/{asin}/sims?similarity_type=InTheSameSeries&response_groups=media", num_results=50)
            for book in books["similar_products"]:
                if book["asin"] in checked or book["asin"] in to_check:
                    continue

                checked.append(book["asin"])

                series = book["publication_name"] if "publication_name" in book else "unknown"
                if series not in new_books:
                    new_books[series] = {}

                checked.append(book["asin"])
                new_books[series][book["asin"]] = book["title"]

    with open(NEW_BOOKS_FILE, "w") as new:
        new.write(json.dumps(new_books, indent="    "))

if __name__ == "__main__":
    main()
