from datetime import timezone

from dateutil.parser import parse
from dateutil.tz import gettz

from datasets.nsw_dataset import NSWSiteParser

parser = NSWSiteParser()
sample_site = {
    "Venue": "Reading Cinema – 6:30pm screening of Fast and Furious 9",
    "Address": "100 Parramatta Road",
    "Suburb": "Auburn",
    "Date": "Sunday 20 June 2021",
    "Time": "6:30pm screening",
    "Alert": "Get tested immediately and self-isolate for 14 days",
    "Lon": "151.044582370374",
    "Lat": "-33.8469128510219",
    "HealthAdviceHTML": "Anyone who attended this venue is a <a href='https://www.health.nsw.gov.au/Infectious/factsheets/Pages/advice-for-contacts.aspx'>close contact</a> and must immediately <a href='https://www.nsw.gov.au/covid-19/how-to-protect-yourself-and-others/clinics'>get tested</a> and <a href='https://www.nsw.gov.au/covid-19/what-you-can-and-cant-do-under-rules/self-isolation'>self-isolate</a> for 14 days regardless of the result, and call 1800 943 553 unless they have already been contacted by NSW Health.",
    "Last updated date": "26/06/2021"
}


def test_to_site():
    site = parser.to_site(sample_site)

    assert site.title == "Reading Cinema – 6:30pm screening of Fast and Furious 9"
    assert site.street_address == "100 Parramatta Road"
    assert site.postcode is None
    assert site.exposure_start_time == parse("2021-06-20T18:30:00 AST",
                                             tzinfos={'AST': gettz('Australia/Sydney')}).astimezone(timezone.utc)
    assert site.exposure_end_time == parse("2021-06-20T23:59:00 AST",
                                           tzinfos={'AST': gettz('Australia/Sydney')}).astimezone(timezone.utc)
    assert site.added_time == parse("2021-06-26T00:00:00 AST",
                                    tzinfos={'AST': gettz('Australia/Sydney')}).astimezone(timezone.utc)


def test_exposure_times():
    test_cases = [
        (
            "6:50am - 8:00am",
            "2021-06-20T06:50:00 AST",
            "2021-06-20T08:00:00 AST",
        ),
        (
            "6:50am to   8:00am",
            "2021-06-20T06:50:00 AST",
            "2021-06-20T08:00:00 AST",
        ),
        (
            "between 8:00am and 8:00pm",
            "2021-06-20T08:00:00 AST",
            "2021-06-20T20:00:00 AST",
        ),
        (
            "1:30pm to 2pm",
            "2021-06-20T13:30:00 AST",
            "2021-06-20T14:00:00 AST",
        ),
        (
            "1.30pm to 2pm",
            "2021-06-20T13:30:00 AST",
            "2021-06-20T14:00:00 AST",
        ),
    ]
    for (time_str, start, end) in test_cases:
        test_data = sample_site.copy()
        test_data['Time'] = time_str

        site = parser.to_site(test_data)
        assert time_str, site.exposure_start_time == parse(start,
                                                           tzinfos={'AST': gettz('Australia/Sydney')}).astimezone(
            timezone.utc)
        assert time_str, site.exposure_end_time == parse(end, tzinfos={'AST': gettz('Australia/Sydney')}).astimezone(
            timezone.utc)


def test_invalid_exposure_date_is_defaulted_to_added_date():
    test_data = sample_site.copy()
    test_data['Date'] = 'Sunday 20 to Monday 21 June 2021'

    site = parser.to_site(test_data)
    assert site.exposure_start_time == parse("2021-06-26T00:00:00 AST",
                                             tzinfos={'AST': gettz('Australia/Sydney')}).astimezone(timezone.utc)
