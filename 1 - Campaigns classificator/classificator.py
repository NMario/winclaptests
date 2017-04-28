#!/usr/bin/python3
from functools import reduce
import json


def load_user():
    return json.load(open('user.json'))


def load_campaigns():
    return json.load(open('campaigns.json'))


def filter_by_plataform(campaigns, user):
    # Filter the campaigns for platform
    return filter(lambda x: x['platform'] == user['platform'], campaigns)


def filter_by_gender(campaigns, user):
    # Filter the campaigns for gender
    return filter(
        lambda x:
            x['gender'] == user['gender'] or
            x['gender'] == 'All',
        campaigns
    )


def filter_by_age(campaigns, user):
    # Filter the campaigns for age
    return filter(
        lambda x:
            (user['age'] >= x['min_age'] or x['min_age'] is None) and
            (user['age'] <= x['max_age'] or x['max_age'] is None),
        campaigns
    )


def filter_by_connection(campaigns, user):
    # Filter the campaigns for connection
    return filter(
        lambda x:
            x['connection'] == user['connection'] or
            x['connection'] == 'All',
        campaigns
    )


def filter_by_age_range(campaigns):
    # Filters the campaigns by age range and returns that which has the
    # age range closer to the user age.
    campaing_age_ranges = []
    for campaign in campaigns:
        if (campaign['max_age'] and campaign['min_age']) is None:
            continue
        campaing_age_ranges.append(campaign)

    if len(campaing_age_ranges) == 0:
        return campaing_age_ranges
    elif len(campaing_age_ranges) > 1:
        selected = reduce(
            lambda x, y:
                x if (x['max_age'] - x['min_age']) <
                     (y['max_age'] - y['min_age']) else y,
            campaing_age_ranges
        )
        return [selected]

# General Filters
filters = [
    filter_by_plataform,
    filter_by_gender,
    filter_by_age,
    filter_by_connection,
]


def get_best_campaign(campaigns, user):
    # General Filters
    filtered = None
    for _filter in filters:
        filtered = _filter(campaigns, user)
        if len(filtered) == 0:
            return None
        campaigns = filtered

    # If there are one or more campaigns, tries to filter them by the age range
    # closer to user age.
    if len(filtered) > 1:
        filtered_by_age_range = []
        if filter_by_age_range(filtered):
            filtered_by_age_range = filter_by_age_range(filtered)
        filtered = filtered_by_age_range if filtered_by_age_range else filtered

    # Next, if there are one or more campaigns, tries to filter them by the
    # user gender.
    if len(filtered) > 1:
        filtered_by_gender = []
        for campaign in filtered:
            if campaign['gender'] == user['gender']:
                filtered_by_gender.append(campaign)
        filtered = filtered_by_gender if filtered_by_gender else filtered

    # Next, if there are one or more campaigns, tries to filter them by
    # the user connection.
    if len(filtered) > 1:
        filtered_by_connection = []
        for campaign in filtered:
            if campaign['connection'] == user['connection']:
                filtered_by_connection.append(campaign)
        filtered = filtered_by_connection if filtered_by_connection else filtered

    # Finally, if after you applied all the filter there are more than one
    # campaings, then selects the first one.
    if len(filtered) >= 1:
        filtered = filtered[0]
    else:
        filtered = None

    return filtered


if __name__ == '__main__':
    campaigns = load_campaigns()
    user = load_user()
    best_campaign = get_best_campaign(campaigns, user)
    print(best_campaign)
