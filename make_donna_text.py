import mailbox
from email.utils import parsedate_to_datetime
from email.header import decode_header, make_header

MBOX = "/data/DONNA_WORK/Donna_Only.mbox"
OUTPUT = "/data/DONNA_WORK/Donna_Letters.txt"


def decode_text_header(value):
    if value is None:
        return ""
    try:
        return str(make_header(decode_header(str(value))))
    except Exception:
        return str(value)


def get_plain_text(msg):
    if msg.is_multipart():

        for part in msg.walk():

            if part.get_content_type() != "text/plain":
                continue

            if part.get_content_disposition() == "attachment":
                continue

            try:
                data = part.get_payload(decode=True)

                charset = part.get_content_charset() or "utf-8"

                if data is not None:
                    return data.decode(charset, errors="replace")

            except Exception:
                pass

    else:
        if msg.get_content_type() == "text/plain":

            try:
                data = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or "utf-8"

                if data is not None:
                    return data.decode(charset, errors="replace")

            except Exception:
                pass

    return "[No plain-text message body found]"


mbox = mailbox.mbox(MBOX)

messages = []

for msg in mbox:

    try:
        dt = parsedate_to_datetime(str(msg.get("Date", "")))
    except (TypeError, ValueError, OverflowError):
        dt = None

    messages.append((dt, msg))


# Sort oldest to newest.
# Messages with unreadable dates go at the end.

messages.sort(
    key=lambda item:
        item[0].timestamp()
        if item[0] is not None
        else float("inf")
)


with open(OUTPUT, "w", encoding="utf-8") as outfile:

    for number, (dt, msg) in enumerate(messages, start=1):

        outfile.write("=" * 78 + "\n")
        outfile.write(f"MESSAGE {number}\n")
        outfile.write("=" * 78 + "\n")

        outfile.write(
            "DATE:    " +
            decode_text_header(msg.get("Date")) +
            "\n"
        )

        outfile.write(
            "FROM:    " +
            decode_text_header(msg.get("From")) +
            "\n"
        )

        outfile.write(
            "TO:      " +
            decode_text_header(msg.get("To")) +
            "\n"
        )

        outfile.write(
            "SUBJECT: " +
            decode_text_header(msg.get("Subject")) +
            "\n"
        )

        outfile.write("\n")

        body = get_plain_text(msg)

        outfile.write(body.rstrip())
        outfile.write("\n\n")


print()
print("Finished.")
print("Messages written:", len(messages))
print("Output:", OUTPUT)