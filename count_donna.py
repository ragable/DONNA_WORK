import mailbox
from collections import defaultdict
from email.utils import parsedate_to_datetime

MBOX = "/data/DONNA_WORK/Takeout/Mail/All mail Including Spam and Trash.mbox"

DONNA = [
    "donnagl@sbcglobal.net",
    "donnagaylindsey@gmail.com",
]

mbox = mailbox.mbox(MBOX)

total = 0
donna_total = 0
from_donna = 0
to_donna = 0

years = defaultdict(lambda: [0, 0])
all_years = defaultdict(int)

for msg in mbox:
    total += 1

    # Count ALL Gmail messages by year
    try:
        dt_all = parsedate_to_datetime(str(msg.get("Date", "")))
        all_years[dt_all.year] += 1
    except (TypeError, ValueError, OverflowError):
        pass

    from_field = str(msg.get("From", "")).lower()
    to_field   = str(msg.get("To", "")).lower()
    cc_field   = str(msg.get("Cc", "")).lower()

    donna_from = any(addr in from_field for addr in DONNA)
    donna_to = any(addr in to_field or addr in cc_field for addr in DONNA)

    if donna_from or donna_to:
        donna_total += 1

    if donna_from:
        from_donna += 1

    if donna_to:
        to_donna += 1

    # Count Donna correspondence by year
    if donna_from or donna_to:
        try:
            dt = parsedate_to_datetime(str(msg.get("Date", "")))
            year = dt.year

            if donna_from:
                years[year][0] += 1

            if donna_to:
                years[year][1] += 1

        except (TypeError, ValueError, OverflowError):
            pass


print()
print("Total messages in Gmail :", total)
print("Messages involving Donna:", donna_total)
print("From Donna              :", from_donna)
print("To/Cc Donna             :", to_donna)

print()
print("DONNA CORRESPONDENCE BY YEAR")
print("----------------------------")
print("YEAR   FROM   TO/CC   TOTAL")
print("---------------------------")

for year in sorted(years):
    frm, to = years[year]
    print(f"{year:<6} {frm:>4}   {to:>5}   {frm + to:>5}")


print()
print("ALL GMAIL BY YEAR")
print("-----------------")

for year in sorted(all_years):
    print(f"{year}: {all_years[year]}")
