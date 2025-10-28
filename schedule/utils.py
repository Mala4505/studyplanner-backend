from hijri_converter import convert
from datetime import timedelta
from .models import StudyBlock

def generate_study_blocks(book, start_date):
    total_pages = book.total_pages
    pages_per_day = (total_pages + book.duration_days - 1) // book.duration_days
    blocks = []

    for i in range(book.duration_days):
        date = start_date + timedelta(days=i)
        hijri = convert.Gregorian(date.year, date.month, date.day).to_hijri()
        page_start = book.page_from + i * pages_per_day
        page_end = min(book.page_to, page_start + pages_per_day - 1)

        blocks.append(StudyBlock(
            book=book,
            # user=book.user,
            date_gregorian=date,
            date_hijri=str(hijri),
            day_of_week=date.strftime('%A'),
            page_start=page_start,
            page_end=page_end
        ))
    return blocks
