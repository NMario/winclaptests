import json


def load_user():
    return json.load(open('user.json'))


def load_campaigns():
    return json.load(open('campaigns.json'))


def get_best_campaign(campaigns, user):

    # Filter the campaigns for platform
    campaigns = filter(lambda x: x['platform'] == user['platform'], campaigns)

    # Filter the campaigns for gender
    campaigns = filter(
        lambda x:
            x['gender'] == user['gender'] or
            x['gender'] == 'All',
        campaigns
    )

    # Filter the campaigns for age
    campaigns = filter(
        lambda x:
            (user['age'] >= x['min_age'] or x['min_age'] == None) and
            (user['age'] <= x['max_age'] or x['max_age'] == None),
        campaigns
    )

    # Filter the campaigns for connection
    campaigns = filter(
        lambda x:
            x['connection'] == user['connection'] or
            x['connection'] == 'All',
        campaigns
    )

    # If there are two o more campaigns, select which one with the small age range.
    if len(campaigns) > 1:
        selected = []
        for campaign in campaigns:
            if (campaign['max_age'] and campaign['min_age']) is None:
                continue
            selected.append(campaign)

        return reduce(
            lambda x, y:
                x if (x['max_age'] - x['min_age']) < (y['max_age'] - y['min_age']) else y,
            selected
        )

    return campaigns[0]

if __name__ == '__main__':

    campaigns = load_campaigns()
    user = load_user()

    best_campaign = get_best_campaign(campaigns, user)
    print(best_campaign)
