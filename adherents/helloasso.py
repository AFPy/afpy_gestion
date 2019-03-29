#!/usr/bin/env python

import csv
from datetime import date, timedelta
from getpass import getpass
from io import StringIO

import requests


LOGIN = 'tresorerie@afpy.org'
CAMPAIGN_IDS = (14589, 31115)


def get_members(year, password=None, output_format='csv'):
    if not password:
        password = getpass('Mot de passe HelloAsso : ')

    session = requests.Session()
    session.get(
        'https://www.helloasso.com/utilisateur/authentificate',
        json={
            'currentUrl': 'https://helloasso.com/',
            'email': LOGIN,
            'password': password,
        }
    )

    start = date(year, 1, 1)
    end = date(year + 1, 1, 1) - timedelta(days=1)

    start_str = f'{start.day}/{start.month}/{start.year}'
    end_str = f'{end.day}/{end.month}/{end.year}'

    for campaign_id in CAMPAIGN_IDS:
        url = (
            'https://www.helloasso.com/admin/handler/reports.ashx?'
            'type=Details&format=Csv&'
            f'id_adh={campaign_id}&from={start_str}&to={end_str}&'
            'includeSubpages=1&period=MONTH&domain=HelloAsso&trans=Adhesions&'
        )
        response = session.get(url)

        rows = csv.reader(StringIO(response.text), delimiter=';')
        header = next(rows)
        name_index = header.index('Nom')
        firstname_index = header.index('Prénom')
        email_index = header.index('Email')

        for row in rows:
            if output_format == 'dict':
                yield {
                    'name': row[name_index],
                    'firstname': row[firstname_index],
                    'email': row[email_index],
                }
            elif output_format == 'csv':
                yield ','.join(
                    row[index] for index in
                    (name_index, firstname_index, email_index)
                )


if __name__ == '__main__':
    password = getpass('Mot de passe HelloAsso : ')

    print('')

    print('Membres de l’année dernière')
    print('===========================')
    print('')
    rows = get_members(date.today().year - 1, password)
    for i, row in enumerate(rows):
        print(f'{i + 4: 3}', row)

    print('')

    print('Membres de cette année')
    print('======================')
    print('')
    rows = get_members(date.today().year, password)
    for i, row in enumerate(rows):
        print(f'{i + 4: 3}', row)
