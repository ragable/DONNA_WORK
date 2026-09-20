import mailbox
import os

SOURCE = "/data/DONNA_WORK/Takeout/Mail/All mail Including Spam and Trash.mbox"
OUTPUT = "/data/DONNA_WORK/Donna_Only.mbox"

DONNA = [
    "donnagl@sbcglobal.net",
    "donnagaylindsey@gmail.com",
]

# Remove an old output file if we're rerunning this program.
if os.path.exists(OUTPUT):
    os.remove(OUTPUT)

source = mailbox.mbox(SOURCE)
output = mailbox.mbox(OUTPUT)

count = 0

for msg in source:

    from_field = str(msg.get("From", "")).lower()
    to_field   = str(msg.get("To", "")).lower()
    cc_field   = str(msg.get("Cc", "")).lower()

    donna_from = any(addr in from_field for addr in DONNA)
    donna_to   = any(addr in to_field or addr in cc_field for addr in DONNA)

    if donna_from or donna_to:
        output.add(msg)
        count += 1

output.flush()
output.close()
source.close()

print()
print("Extraction complete.")
print("Messages written:", count)
print("Output:", OUTPUT)