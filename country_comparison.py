import csv
import sys
from matplotlib import pyplot as plt
import datetime


def main():
    if len(sys.argv) != 2:
        print("One (1) argument expected: <filename>. Number of arguments received:", len(sys.argv)-1)
        exit(1)

    country_date_dict, country_agg_dict, country_perc_dict = parse_csv_input(sys.argv[1])

    countries = list(country_date_dict.keys())
    for country in countries:
        if country in country_date_dict.keys() and country in country_agg_dict.keys() and country in country_perc_dict.keys():
            date_d, agg_d, perc_d = country_date_dict[country], country_agg_dict[country], country_perc_dict[country]

            m = max(agg_d.keys())
            if agg_d[m][0] > 100:
                print_country_data(country, date_d, agg_d, perc_d)


def parse_csv_input(filename):

    countries_data_by_date = {}
    countries_pop_data = {}
    """
    0 dateRep
    1 day
    2 month
    3 year
    4 cases
    5 deaths
    6 countriesAndTerritories
    7 geoId
    8 countryterritoryCode
    9 popData2018
    """

    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        # for index, column_header in enumerate(header_row):
        #     print(index, column_header, end=' ')
        # else:
        #     print()

        for row in reader:
            if row[9] and row[6] not in countries_pop_data.keys():
                countries_pop_data[row[6]] = int(row[9])
            if row[6] not in countries_data_by_date.keys():
                countries_data_by_date[row[6]] = {}

            if row[3] != '2020':
                continue
            fmt = '%d/%m/%Y'
            tt = datetime.datetime.strptime(row[0], fmt).timetuple()
            countries_data_by_date[row[6]][tt.tm_yday] = int(row[4]), int(row[5])

    countries_agg_data_by_date = {}
    countries_percent_agg_data_by_date = {}
    for country in countries_pop_data.keys():
        countries_agg_data_by_date[country] = {}
        countries_percent_agg_data_by_date[country] = {}
        agg_cases, agg_deaths = 0, 0
        for jdate in sorted(countries_data_by_date[country].keys()):
            agg_cases += countries_data_by_date[country][jdate][0]
            agg_deaths += countries_data_by_date[country][jdate][1]
            countries_agg_data_by_date[country][jdate] = agg_cases, agg_deaths
            countries_percent_agg_data_by_date[country][jdate] = agg_cases / countries_pop_data[country], agg_deaths / countries_pop_data[country]

    return countries_data_by_date, countries_agg_data_by_date, countries_percent_agg_data_by_date


def print_country_data(country, data_by_date, agg_data_by_date, percent_agg_data_by_date):
    def first_date(dates, dictionary):
        first = -1
        for i,d in enumerate(dates):
            if dictionary[d][0] > 0:
                first = i
                break
        for d in range(first-1, dates[0]-1, -1):
            if d in dictionary.keys():
                del dictionary[d]
        return first, dictionary

    print("Making plot for", country)
    dates = sorted(data_by_date.keys())
    first, data = first_date(dates, data_by_date)
    dates = dates[first:]

    cases = [data[x][0] for x in dates]
    deaths = [data[x][1] for x in dates]

    agg_data = agg_data_by_date
    agg_cases = [agg_data[x][0] for x in dates]
    agg_deaths = [agg_data[x][1] for x in dates]

    perc_data = percent_agg_data_by_date
    perc_cases = [perc_data[x][0] for x in dates]
    perc_deaths = [perc_data[x][1] for x in dates]

    # print(country, cases, agg_cases, perc_cases)

    fig = plt.figure(dpi=256, figsize=(10, 6))
    plt.plot(dates, cases, marker='', color='black')
    plt.plot(dates, deaths, marker='', color='red')
    plt.plot(dates, agg_cases, marker='', color='black', linestyle='dashed')
    plt.plot(dates, agg_deaths, marker='', color='red', linestyle='dashed')
    plt.plot(dates, perc_cases, marker='', color='orange')
    plt.title(country + " 2020", fontsize=24)
    plt.xlabel('Julian Date', fontsize=16)
    plt.ylabel("", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)

    # plt.show()
    plt.savefig('./countries/' + country + '-3plot.png')


if __name__ == '__main__':
    main()

"""
    countries need more work:
    albania
    argentina
    bangladesh
"""