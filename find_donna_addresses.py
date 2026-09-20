import mailbox
from email.utils import getaddresses

MBOX = "/data/DONNA_WORK/Takeout/Mail/All mail Including Spam and Trash.mbox"

mbox = mailbox.mbox(MBOX)

addresses = set()

for msg in mbox:

    headers = []

    headers.extend(msg.get_all("From", []))
    headers.extend(msg.get_all("To", []))
    headers.extend(msg.get_all("Cc", []))

    for name, address in getaddresses([str(x) for x in headers]):

        name_lower = name.lower()
        address_lower = address.lower()

        if "donna" in name_lower or "lindsey" in name_lower:
            addresses.add((name, address_lower))


print()
print("ADDRESSES ASSOCIATED WITH DONNA/LINDSEY")
print("---------------------------------------")

for name, address in sorted(addresses):
    print(f"{name:<30} {address}")It's 