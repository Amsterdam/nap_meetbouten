from decimal import Decimal


# cleanup row as returned from csv parser
def cleanup_row(csv_row, replace=False):
    row = list()
    for i in range(0, len(csv_row)):
        val = csv_row[i]

        # het kenmerk 'omschrijving' bevat karakters chr13 (=carriage return)
        # en ^10 (=line feed). Deze moeten terug gecodeerd worden.
        if replace:
            val = val.replace("^10", "\n")
            val = val.replace("chr13", "\r")

        # the double quotes setting with $ is not working like I would like it to
        if val[-2:] == '$$':
            val = val[0:len(val)-2]

        if val == '$':
            val = ''

        row.append(val.strip())

    return row


def parse_decimal(d):
    return Decimal(d.replace(',', '.'))
