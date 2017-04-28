#!/usr/bin/python3
from html.parser import HTMLParser
import re
import json
import urllib.request


class CurrencyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = False
        self.data = None

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'bld':
                    self.recording = True

    def handle_endtag(self, tag):
        if tag == 'span':
            self.recording = False

    def handle_data(self, data):
        if self.recording:
            match = re.match(r'\d+(\.\d+)*\s[A-Z]{3}', data)
            if match:
                self.data = match.group(0)


def load_daily_report():
    return json.load(open('campaigns.json'))


def convert_currency(amount, _from, to):
    URL = 'https://www.google.com/finance/converter?a={0}&from={1}&to={2}'

    with urllib.request.urlopen(URL.format(amount, _from, to)) as f:
        p = CurrencyHTMLParser()
        p.feed(str(f.read()))
        p.close()
        return p.data


def get_total_profit(campaign):
    # Calcuate the profit of the campaign
    profit = campaign['revenue'] - campaign['cost']

    # Calcuate the total profit of the campaign
    total_profit = profit * campaign['conversions']

    return total_profit


def generate_total_profits_report(campaings):
    results = []
    for campaign in campaigns:

        total_profit = get_total_profit(campaign)

        # Convert the total profit in USD
        if campaign['currency'] != 'USD':
            total_profit = convert_currency(total_profit, campaign['currency'], 'USD')

        results.append({
            'id': campaign['id'],
            'name': campaign['name'],
            'total_profit': total_profit
        })
    return results


if __name__ == '__main__':
    campaigns = load_daily_report()
    final_report = generate_total_profits_report(campaigns)
    print(final_report)
