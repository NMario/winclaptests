#!/usr/bin/python3
from functools import reduce
import json


def load_user():
    return json.load(open('user.json'))


def load_campaigns():
    return json.load(open('campaigns.json'))


def filter_by_plataform(campaigns):
    # Filter the campaigns for platform
    return filter(lambda x: x['platform'] == user['platform'], campaigns)


def filter_by_gender(campaigns):
    # Filter the campaigns for gender
    return filter(
        lambda x:
            x['gender'] == user['gender'] or
            x['gender'] == 'All',
        campaigns
    )


def filter_by_age(campaigns):
    # Filter the campaigns for age
    return filter(
        lambda x:
            (user['age'] >= x['min_age'] or x['min_age'] is None) and
            (user['age'] <= x['max_age'] or x['max_age'] is None),
        campaigns
    )


def filter_by_connection(campaigns):
    # Filter the campaigns for connection
    return filter(
        lambda x:
            x['connection'] == user['connection'] or
            x['connection'] == 'All',
        campaigns
    )


def filter_by_age_range(campaigns):
    campaing_age_ranges = []
    for campaign in campaigns:
        if (campaign['max_age'] and campaign['min_age']) is None:
            continue
        campaing_age_ranges.append(campaign)

    if len(campaing_age_ranges) == 0:
        return campaing_age_ranges
    elif len(campaing_age_ranges) > 1:
        return reduce(
            lambda x, y:
                x if (x['max_age'] - x['min_age']) < (y['max_age'] - y['min_age']) else y,
            campaing_age_ranges
        )


filters = [
    filter_by_plataform,
    filter_by_gender,
    filter_by_age,
    filter_by_connection,
    filter_by_age_range
]


def get_best_campaign(campaigns, user):
    best_campaign = None

    selected = []
    for _filter in filters:
        selected = _filter(campaigns)
        if len(selected) == 0:
            return best_campaign
        elif len(selected) == 1:
            return selected[0]
        else:
            campaigns = selected


if __name__ == '__main__':

    campaigns = load_campaigns()
    user = load_user()

    best_campaign = get_best_campaign(campaigns, user)
    print(best_campaign)
