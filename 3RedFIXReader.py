#
# File: FIXReader.py
# Author: blee4
# Date: 25 April 2018
# Purpose: Create a FIX parser and answer the following questions:
#           1. How many instruments of each security type (tag 167) exist?
#           2. How many futures (tag 167) instruments exist in each product complex (tag 462)?
#           3. What are the names (tag 55) of the earliest four expirations (tag 200) for the futures (tag 167)
#               instruments with asset (tag 6937) 'GE' and have zero legs (tag 555)?
#
from operator import itemgetter


# Name: parse_secdef
# Input: filename; FIX formatted data file (must be in the same directory as the .py)
# Output: market_data; Parsed FIX data
# Purpose: To parse the FIX formatted file
def parse_secdef(filename):
    market_data = {}
    with open(filename) as f:
        for index, line in enumerate(f):
            market_data.setdefault(index, {})
            line = line.split('\x01')
            for entry in line:
                # Check to see if the 'entry' is a sole '\n' character; if so, filter it out
                if len(entry) > 1:
                    entry = entry.split('=')
                    category = {entry[0]: entry[1]}
                    market_data[index].update(category)
                else:
                    continue
    f.close()
    return market_data


# Name: security_type_count
# Input: parsed_data; Parsed FIX data
# Output: None
# Purpose: To count the number of each security type
def security_type_count(parsed_data):
    count_fut = count_oof = count_mleg = count_irs = count_unknown = 0
    for i in parsed_data:
        if '167' in data[i]:
            if 'FUT' == data[i]['167']:
                count_fut += 1
            elif 'OOF' == data[i]['167']:
                count_oof += 1
            elif 'MLEG' == data[i]['167']:
                count_mleg += 1
            elif 'IRS' == data[i]['167']:
                count_irs += 1
        else:
            count_unknown += 1
    print("----------Security Type Count----------")
    print("FUT: %d" % count_fut)
    print("OOF: %d" % count_oof)
    print("MLEG: %d" % count_mleg)
    print("IRS: %d" % count_irs)
    print("Unknown: %d" % count_unknown)
    print("Total Security Count: %d" % (count_fut + count_oof + count_mleg + count_irs + count_unknown))
    print()


# Name: product_type_count
# Input: parsed_data; Parsed FIX data
#        security; Security type (refer to Tag 167)
# Output: None
# Purpose: To find the product complex type within the specified security type
def product_type_count(parsed_data, security):
    count_commodity = count_currency = count_equity = count_other = count_interest = count_fx = count_energy = 0
    count_metals = count_unknown = 0
    for j in parsed_data:
        if security == data[j]['167']:
            if '462' in data[j]:
                if '2' == data[j]['462']:
                    count_commodity += 1
                elif '4' == data[j]['462']:
                    count_currency += 1
                elif '5' == data[j]['462']:
                    count_equity += 1
                elif '12' == data[j]['462']:
                    count_other += 1
                elif '14' == data[j]['462']:
                    count_interest += 1
                elif '15' == data[j]['462']:
                    count_fx += 1
                elif '16' == data[j]['462']:
                    count_energy += 1
                elif '17' == data[j]['462']:
                    count_metals += 1
            else:
                count_unknown += 1
        else:
            continue
    print("----------Product Complex Type Count for %s----------" % security)
    print("Commodity/Agriculture: %d" % count_commodity)
    print("Currency: %d" % count_currency)
    print("Equity: %d" % count_equity)
    print("Other: %d" % count_other)
    print("Interest Rate: %d" % count_interest)
    print("FX Cash: %d" % count_fx)
    print("Energy: %d" % count_energy)
    print("Metals: %d" % count_metals)
    print("Unknowns: %d" % count_unknown)
    print()


# Name: question_three
# Input: parsed_data; Parsed FIX data
#        security; Security type (refer to Tag 167)
#        asset; Asset type (refer to Tag 6937)
#        legs; Number of legs (refer to Tag 555)
# Output: None
# Purpose: To find four securities with earliest expirations that fits into a specific search criteria
def question_three(parsed_data, security, asset, legs):
    odd_days = ['1', '3', '5', '7', '8', '10', '12']
    even_days = ['4', '6', '9', '11']
    filtered = []
    for k in parsed_data:
        if security == data[k]['167']:
            if '6937' in data[k] and '555' in data[k]:
                if (asset == data[k]['6937']) and (legs == data[k]['555']):
                    year = data[k]['200'][:4]
                    month = data[k]['200'][4:6]
                    if len(data[k]['200']) == 6:
                        # This assumes that the monthlies and quarterlies expire at the end of the month (business day)
                        # YYYYMM
                        if month == '2':
                            filtered.append((year, month, '28', data[k]['55']))
                        elif month in odd_days:
                            filtered.append((year, month, '31', data[k]['55']))
                        elif month in even_days:
                            filtered.append((year, month, '30', data[k]['55']))
                        # This assumes that the month begins on the 1st and increase in multiples of 7; for weeklies
                        # YYYYMMwN
                    elif data[k]['200'][6:7] == 'w':
                        # Week 5 will end on the last business day of the month
                        if data[k]['200'][7:8] == '5':
                            filtered.append((year, month, 31, data[k]['55']))
                        else:
                            filtered.append((year, month, data[k]['200'][7:8] * 7, data[k]['55']))
                        # This is for securities with exact maturity date
                        # YYYYMMDD
                    else:
                        filtered.append((year, month, data[k]['200'][6:8], data[k]['55']))
                else:
                    continue
    filtered.sort(key=itemgetter(0, 1, 2))
    print("--------%s with Earliest Four Expirations for asset '%s' and legs: '%s'--------" % (security, asset, legs))
    if not len(filtered) > 1:
        print("There are no matches for your search criteria!")
    else:
        for l in filtered[:4]:
            print("Symbol: %s\tExpires on: %s/%s/%s" % (l[3], l[0], l[1], l[2]))
    print()


# Call functions and execute main code
data = parse_secdef('secdef.dat')
security_type_count(data)
product_type_count(data, 'FUT')
question_three(data, 'FUT', 'GE', '0')
