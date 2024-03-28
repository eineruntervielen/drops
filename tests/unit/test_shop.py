import unittest

from drops import Drops
from tests.examples.shop import customer_logging
from tests.examples.shop.checkout_area import CheckoutArea
from tests.examples.shop.checkout_source import checkout_source_gen
from tests.examples.shop.customer_source import customer_source_gen
from tests.examples.shop.payment_area import PaymentArea


class AllExamplesTest(unittest.TestCase):
    def test_example_shop(self):
        drops = Drops()
        drops.register_source(customer_source_gen(num_customer=50), "customer_arrives", call_initial=True)
        drops.register_source(checkout_source_gen(num_checkout=1), "register_checkout", call_initial=True)
        drops.register_instance(PaymentArea())
        drops.register_instance(CheckoutArea())
        drops.register_module(customer_logging)
        drops.run()


if __name__ == '__main__':
    unittest.main()
