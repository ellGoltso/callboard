from django.shortcuts import render

from django.template.loader import get_template
print(get_template('registration/password_reset_email.txt').origin)
