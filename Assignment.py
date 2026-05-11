import asyncio
from datetime import datetime, timedelta
from typing import List, Dict

books_db: List[Dict] = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "John Smith",
        "category": "Programming",
        "status": "Available"
    },
    {
        "id": 2,
        "title": "Database Systems",
        "author": "Mary Johnson",
        "category": "Technology",
        "status": "Available"
    }
]

borrow_records: List[Dict] = []

FINE_PER_DAY: float = 0.50
LOAN_PERIOD_DAYS: int = 14

# SEARCH BOOKS
async def search_books(keyword: str,
                       search_by: str = "title") -> Dict:

    await asyncio.sleep(0)

    results = [
        book for book in books_db
        if keyword.lower() in book.get(search_by, "").lower()
    ]

    return {
        "status": "Success",
        "results_found": len(results),
        "books": results
    }

# BORROW BOOK
async def borrow_book(book_id: int,
                      student_name: str) -> Dict:

    await asyncio.sleep(0)

    for book in books_db:

        if book["id"] == book_id and book["status"] == "Available":

            book["status"] = "Borrowed"

            due_date = datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)

            borrow_records.append({
                "book_id": book_id,
                "student_name": student_name,
                "due_date": due_date.strftime("%Y-%m-%d")
            })

            return {
                "status": "Success",
                "message": "Book borrowed successfully",
                "due_date": due_date.strftime("%Y-%m-%d")
            }

    return {
        "status": "Failed",
        "message": "Book unavailable"
    }

# RETURN BOOK
async def return_book(book_id: int,
                      student_name: str) -> Dict:

    await asyncio.sleep(0)

    for record in borrow_records:

        if record["book_id"] == book_id and \
           record["student_name"] == student_name:

            for book in books_db:

                if book["id"] == book_id:
                    book["status"] = "Available"

            due_date = datetime.strptime(
                record["due_date"],
                "%Y-%m-%d"
            )

            overdue_days = (datetime.now() - due_date).days

            fine = max(0, overdue_days * FINE_PER_DAY)

            borrow_records.remove(record)

            return {
                "status": "Returned",
                "fine": f"${fine:.2f}" if fine > 0 else "No Fine"
            }

    return {
        "status": "Failed",
        "message": "Borrow record not found"
    }

# OVERDUE BOOKS
async def overdue_books() -> Dict:

    await asyncio.sleep(0)

    today = datetime.now()

    overdue_list = []

    for record in borrow_records:

        due_date = datetime.strptime(
            record["due_date"],
            "%Y-%m-%d"
        )

        if today > due_date:

            days = (today - due_date).days

            overdue_list.append({
                **record,
                "fine_owed": f"${days * FINE_PER_DAY:.2f}"
            })

    return {
        "status": "Success",
        "overdue_books": overdue_list
    }

# MULTIPLE USERS SIMULATION
async def simulate_users():

    results = await asyncio.gather(

        borrow_book(1, "Abdulai Kamara"),
        borrow_book(2, "Fatima Sesay"),
        borrow_book(1, "Mohamed Bangura")
    )

    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(simulate_users())
