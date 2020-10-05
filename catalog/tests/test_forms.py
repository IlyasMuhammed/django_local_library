import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookModelForms


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookModelForms()
        self.assertTrue(form.fields['due_back'].label == None or form.fields['due_back'].label == 'Due Back')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookModelForms()
        self.assertEqual(form.fields['due_back'].help_text, 'Due back date')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookModelForms(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookModelForms(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookModelForms(data={'due_back': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookModelForms(data={'due_back': date})
        self.assertTrue(form.is_valid())