import unittest
from decimal import Decimal
from dao.ProductDAO import ProductDAO
from log.log import get_logger

class TestProductDAO(unittest.TestCase):
    def setUp(self):
        # create a new product before each test
        self.logger = get_logger(__name__)
        self.logger.info("Setting up test environment for ProductDAO...")
        self.test_product_name = "Test Product"
        self.test_price = 19.99
        self.test_inventory = 50
        self.test_category = "Test Category"
        self.test_description = "A test product for unit testing."
        self.new_product_id = ProductDAO.create_product(
            self.test_product_name,
            self.test_price,
            self.test_inventory,
            self.test_category,
            self.test_description
        )

    def tearDown(self):
        # delete product after each test
        self.logger.info("Tearing down test environment for ProductDAO...")
        if self.new_product_id:
            deleted = ProductDAO.delete_product_by_id(self.new_product_id)
            if deleted == 0:
                self.logger.warning(f"Product with ID {self.new_product_id} not found during teardown.")
            self.assertEqual(deleted, 1, f"Failed to delete product during teardown (ID: {self.new_product_id})")

    def test_create_product(self):
        # test create new product
        self.assertIsNotNone(self.new_product_id, "Failed to create product")
        product = ProductDAO.get_product_by_id(self.new_product_id)
        self.assertIsNotNone(product, "Product should exist after creation")
        self.assertEqual(product.name, self.test_product_name)

    def test_update_inventory(self):
        # test update product inventory
        new_inventory = 100
        updated = ProductDAO.update_inventory_by_id(self.new_product_id, new_inventory)
        self.assertEqual(updated, 1, "Failed to update inventory")
        product = ProductDAO.get_product_by_id(self.new_product_id)
        self.assertEqual(product.inventory, new_inventory, "Inventory update failed")

    def test_update_price(self):
        # test update product price
        new_price = 49.99
        updated = ProductDAO.update_price_by_id(self.new_product_id, new_price)
        self.assertEqual(updated, 1, "Failed to update price")
        product = ProductDAO.get_product_by_id(self.new_product_id)
        self.assertEqual(product.price, Decimal(str(new_price)), "Price update failed")

    def test_delete_product(self):
        # test delete product
        deleted = ProductDAO.delete_product_by_id(self.new_product_id)
        self.assertEqual(deleted, 1, f"Failed to delete product (ID: {self.new_product_id})")
        product = ProductDAO.get_product_by_id(self.new_product_id)
        self.assertIsNone(product, "Product should not exist after deletion")
        self.new_product_id = None  # 避免 tearDown 再次尝试删除

if __name__ == '__main__':
    unittest.main()
