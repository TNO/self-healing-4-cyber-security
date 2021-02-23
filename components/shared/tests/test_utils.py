import unittest
from unittest import mock

from sh4cs_common.utils import get_container_name


class TestContainerName(unittest.TestCase):
    @mock.patch("sh4cs_common.utils.os")
    def test_container_name(self, os_mock):
        os_mock.environ.get.return_value = "random_name"
        name = get_container_name()
        self.assertEqual("random_name", name)

        # Verify caching works
        os_mock.environ.get.return_value = "random_name"
        self.assertEqual(get_container_name(), name)


if __name__ == "__main__":
    unittest.main()
