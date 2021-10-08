from rest_framework.test import APITestCase
from plan.model import Plan


class TestAccountModel(APITestCase):

    def test_create_plan_account(self):
        plan = Plan.objects.create(plan_name='Basic')

        self.assertEqual(plan.__str__(), str(plan))
        plan.delete()
