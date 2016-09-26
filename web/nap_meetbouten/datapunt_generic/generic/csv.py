from decimal import Decimal, InvalidOperation


# cleanup row as returned from csv parser
def cleanup_row(csv_row, replace=False):
    row = list()
    for i in range(0, len(csv_row)):
        val = csv_row[i]

        # replace(replace(replace(:BOUT_NR,'^10',chr(10)),'^13',chr(13)),'^36',chr(36))
        if replace:
            val = val.replace("^10", chr(10))
            val = val.replace("chr13", chr(13)).replace("^13", chr(13))
            val = val.replace("^36", chr(36))

        # the double quotes setting with $ is not working like I would like it to
        if val[-2:] == '$$':
            val = val[0:len(val)-2]

        if val == '$':
            val = ''

        row.append(val.strip())

    return row


def parse_decimal(d):
    d = '0' if d == '' else d

    try:
        return Decimal(d.replace(',', '.'))
    except InvalidOperation:
        return Decimal()
