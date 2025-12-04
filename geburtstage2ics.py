# ##########################################################################################
# Hans Straßgütl
#       Mein Ersatz für die langjährige REXX um Geburtstagseinträge im Kalender zu erstellen.
#       * Benötigt eine geburtstage.txt als Eingabe
#       * Editiere zuerst die Geburtstage.txt. Das stellt sicher, dass in kommenden Jahr nur die 
#           Geburtsage derer sind, an denen du noch Interesse hast.
#       * Fragt nach dem zu erstellenden Jahr.    
#       * Schreibt eine geburtsage.ics    
#       * Drag & Drop in den emClient Kalender. So du sie dort wieder rauslöschen willst: 
#           - Kalenderdarstellung: Agenda - sortiere nach "Erstellt" ooder "Aktualisiert"
#           
# ------------------------------------------------------------------------------------------
# Version:
#	2025 12 03		Ersterstellung.
#
# ##########################################################################################

import datetime

def read_birthdays(filename):
    birthdays = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(";"):
                continue  # Kommentar oder leer → überspringen

            # Format: YYYY.MM.DD Name ...
            try:
                date_part, name = line.split(" ", 1)
                year, month, day = date_part.split(".")
                birthdays.append({
                    "year": year,
                    "month": month,
                    "day": day,
                    "name": name.strip()
                })
            except ValueError:
                print(f"⚠️ Zeile übersprungen (ungültig): {line}")
                continue
    return birthdays


def create_ics(year, birthdays, output_file="geburtstage.ics"):
    ics = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//HaSt ICS Wandler / 001",
        "X-LOTUS-CHARSET:UTF-8",
        "METHOD:PUBLISH"
    ]

    uid_counter = 1

    for b in birthdays:
        created = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        dt_start = datetime.date(int(year), int(b['month']), int(b['day']))
        dt_end = dt_start + datetime.timedelta(days=1)

        dtstart = dt_start.strftime("%Y%m%d")
        dtend = dt_end.strftime("%Y%m%d")

        # summary = f"<<Geburtstag>>\\n{b['name']} {b['day']}.{b['month']}.{b['year']}\\n"
        summary = f"<<Geburtstag>>{b['name']} {b['day']}.{b['month']}.{b['year']}"

        event = [
            "BEGIN:VEVENT",
            f"UID:Geburtstage-{year}-{uid_counter}",
            f"CREATED:{created}",
            f"DTSTART;VALUE=DATE:{dtstart}",
            f"DTEND;VALUE=DATE:{dtend}",
            f"SUMMARY:{summary}",
            "TRANSP:TRANSPARENT",
            "CLASS:PRIVATE",
            "X-MICROSOFT-CDO-ALLDAYEVENT:TRUE",
            "X-FUNAMBOL-ALLDAY:TRUE",
            "CATEGORIES:Birthday",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "DESCRIPTION:Alarm",
            "TRIGGER;RELATED=START:-PT18H",
            "END:VALARM",
            "END:VEVENT"
        ]

        uid_counter += 1
        ics.extend(event)

    ics.append("END:VCALENDAR")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ics))
    print(f"✔ ICS-Datei erzeugt: {output_file}")


if __name__ == "__main__":
    jahr = input("Für welches Jahr sollen die Geburtstage erzeugt werden? ")

    birthdays = read_birthdays("geburtstage.txt")
    create_ics(jahr, birthdays)
