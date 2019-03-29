#!/usr/bin/env python

import smtplib
import sys
import time
import traceback
from datetime import date
from email.message import EmailMessage
from getpass import getpass

from helloasso import get_members


HOST = 'mail.afpy.org'
PORT = 587
SUBJECT = 'Campagne de cotisation AFPy'
TEMPLATE = '''Bonjour {firstname} {name},

Vous recevez ce courriel en tant que membre de l'Association Francophone
Python.

Nos scripts Python nous ont informés que vous n'étiez pas à jour de votre
cotisation.

Maintenir votre cotisation à jour vous permet de prendre part aux votes lors
des assembles générales et de soutenir l'action de l'association,
financièrement et moralement.

Voici un exemple des ralisations de l'AFPy ces dernières années :

- organisation des confrences PyConFr,
- partenariat avec la confrence PyData,
- financement ou organisation de divers ateliers Python (Django Girl, Django
  Carrot. Workshop Django…),
- traduction en français de la documentation Python,
- mise en place de rencontres locales (Lyon, Pau, Nantes, Grenoble, Paris,
  Rennes…).

La cotisation annuelle de l'AFPy est de 20 €. Le taux réduit de 10 € s'applique
aux personnes ayant des revenus modestes.

Vous pouvez payer votre cotisation en ligne à l'adresse suivante :

    https://www.helloasso.com/associations/afpy/adhesions/

En attendant de recevoir votre cotisation, nous vous souhaitons une bonne
journée pleine de Python !

-- 
Association Francophone Python
'''


if __name__ == '__main__':
    smtp_login = getpass('Identifiant SMTP : ')
    smtp_password = getpass('Mot de passe SMTP : ')
    hello_password = getpass('Mot de passe HelloAsso : ')

    print()
    print('Récupération des membres…')
    print()

    old_members = get_members(
        date.today().year - 1, hello_password, output_format='dict')
    new_members_emails = {
        member['email'] for member in
        get_members(date.today().year, hello_password, output_format='dict')}
    members = [
        member for member in old_members
        if member['email'] not in new_members_emails]

    members = [{'firstname': 'Guillaume', 'name': 'Ayoub', 'email': 'xovni@wanadoo.fr'}]
    print(f'Envoi du message à {len(members)} personnes dans 10 secondes !')
    print()
    time.sleep(10)

    for member in members:
        message = EmailMessage()
        message.set_content(TEMPLATE.format(**member))
        message['Subject'] = SUBJECT
        message['From'] = f'Association Francophone Python <{smtp_login}>'
        message['To'] = [member['email']]

        print(f'Envoi à {member["email"]}')

        afpy_smtp = smtplib.SMTP(host=HOST, port=PORT)
        afpy_smtp.starttls()
        afpy_smtp.login(smtp_login, smtp_password)
        try:
            afpy_smtp.send_message(message)
        except Exception:
            traceback.print_exc(file=sys.stderr)
        afpy_smtp.quit()
        time.sleep(1)
