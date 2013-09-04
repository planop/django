from __future__ import unicode_literals

from django.test import TestCase

from .models import Secondary, Primary


class RefreshTests(TestCase):

    def test_refresh(self):
        s1 = Secondary.objects.create(name="x1")
        p1 = Primary.objects.create(name="p1", value="xx", related=s1)

        a = Primary.objects.get(pk = p1.pk)
        b = Primary.objects.get(pk = p1.pk)

        self.assertEqual(a.name, "p1")
        self.assertEqual(b.name, "p1")
        a.name = "p2"
        a.save()
        self.assertEqual(a.name, "p2")
        self.assertEqual(b.name, "p1")
        b.refresh()
        self.assertEqual(b.name, "p2")

    def test_refresh_fields(self):
        s1 = Secondary.objects.create(name="x1")
        p1 = Primary.objects.create(name="p1", value="xx", related=s1)

        a = Primary.objects.get(pk = p1.pk)
        b = Primary.objects.get(pk = p1.pk)

        self.assertEqual(a.name, "p1")
        self.assertEqual(b.name, "p1")
        self.assertEqual(a.value, "xx")
        self.assertEqual(b.value, "xx")
        a.name = 'p2'
        a.value = 'yy'
        a.save()
        self.assertEqual(a.name, "p2")
        self.assertEqual(b.name, "p1")
        self.assertEqual(a.value, "yy")
        self.assertEqual(b.value, "xx")
        b.refresh('name')
        self.assertEqual(b.name, "p2")
        self.assertEqual(b.value, "xx")
        b.refresh('value')
        self.assertEqual(b.name, "p2")
        self.assertEqual(b.value, "yy")

    def test_refresh_related(self):
        s1 = Secondary.objects.create(name="x1")
        s2 = Secondary.objects.create(name="x2")
        p1 = Primary.objects.create(name="p1", value="xx", related=s1)

        a = Primary.objects.get(pk = p1.pk)
        b = Primary.objects.get(pk = p1.pk)

        self.assertEqual(a.related, s1)
        self.assertEqual(b.related, s1)
        a.related = s2
        a.save()
        self.assertEqual(a.related, s2)
        self.assertEqual(b.related, s1)
        b.refresh()
        self.assertEqual(b.related, s2)

    def test_refresh_related_fields(self):
        s1 = Secondary.objects.create(name="x1")
        s2 = Secondary.objects.create(name="x2")
        p1 = Primary.objects.create(name="p1", value="xx", related=s1)

        a = Primary.objects.get(pk = p1.pk)
        b = Primary.objects.get(pk = p1.pk)

        self.assertEqual(a.related, s1)
        self.assertEqual(b.related, s1)
        a.related = s2
        a.save()
        self.assertEqual(a.related, s2)
        self.assertEqual(b.related, s1)
        b.refresh('related')
        self.assertEqual(b.related, s2)
        b.related = s1
        self.assertEqual(b.related, s1)
        b.refresh('related_id')
        self.assertEqual(b.related, s2)

    def test_refresh_invalid_fieldname(self):
        s1 = Secondary.objects.create(name="x1")
        p1 = Primary.objects.create(name="p1", value="xx", related=s1)

        a = Primary.objects.get(pk = p1.pk)
        b = Primary.objects.get(pk = p1.pk)
        self.assertRaises(ValueError, b.refresh(),'nofield')
