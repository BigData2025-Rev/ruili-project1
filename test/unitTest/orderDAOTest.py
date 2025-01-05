import unittest
from dao.OrderDAO import OrderDAO
from log.log import get_logger

class TestOrderDAO(unittest.TestCase):
    def setUp(self):
        # create a new product before each test
        self.logger = get_logger(__name__)
        self.logger.info("Setting up test environment for OrderDAO...")

        # existing user and product for test
        self.test_user_id = 19 
        self.test_product_id = 26 
        self.test_quantity = 2 

        # create new order
        self.new_order_id = OrderDAO.create_order(
            self.test_user_id, self.test_product_id, self.test_quantity
        )

    def tearDown(self):
        # delete the order after each test
        self.logger.info("Tearing down test environment for OrderDAO...")
        if self.new_order_id:
            deleted = OrderDAO.delete_order_by_id(self.new_order_id)
            self.assertEqual(deleted, 1, "Failed to delete order during teardown")


    def test_create_order(self):
        # test create new order
        self.assertIsNotNone(self.new_order_id, "Failed to create order")
        order = OrderDAO.get_order_by_id(self.new_order_id)
        self.assertIsNotNone(order, "Order should exist after creation")
        self.assertEqual(order.quantity, self.test_quantity, "Order quantity mismatch")
        self.assertEqual(order.user_id, self.test_user_id, "Order user_id mismatch")
        self.assertEqual(order.product_id, self.test_product_id, "Order product_id mismatch")

    def test_get_orders_by_user(self):
        # test get order
        orders = OrderDAO.get_orders_by_user(self.test_user_id)
        self.assertGreater(len(orders), 0, "No orders found for user")
        self.assertEqual(orders[0].user_id, self.test_user_id, "User ID mismatch in orders")

if __name__ == '__main__':
    unittest.main()
