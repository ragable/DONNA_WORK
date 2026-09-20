import mailbox

MBOX = "/data/DONNA_WORK/Donna_Only.mbox"

mbox = mailbox.mbox(MBOX)

for number, msg in enumerate(mbox):

    if number >= 10:
        break

    print()
    print("=" * 70)
    print("MESSAGE", number + 1)
    print("=" * 70)

    print("Date:   ", msg.get("Date", ""))
    print("From:   ", msg.get("From", ""))
    print("To:     ", msg.get("To", ""))
    print("Subject:", msg.get("Subject", ""))

    print("Multipart:", msg.is_multipart())
    print("Content-Type:", msg.get_content_type())

    if msg.is_multipart():
        print("Parts:")

        for part in msg.walk():
            print(
                "   ",
                part.get_content_type(),
                "disposition =",
                part.get_content_disposition()
            )
