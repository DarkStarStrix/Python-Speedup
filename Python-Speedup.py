import unittest
from unittest.mock import patch, MagicMock
from main import RustPythonIntegration


class TestRustPythonIntegration (unittest.TestCase):
    @patch ('main.rust_computation_wrapper', return_value=1)
    @patch ('main.ProcessPoolExecutor')
    def successful_computation(self, mock_executor, mock_computation):
        # Given
        mock_executor.return_value.__enter__.return_value.map.return_value = [1, 2, 3, 4]
        data = [1, 2, 3, 4]
        rust_python_integration = RustPythonIntegration ()

        # When
        asyncio.run (rust_python_integration.main_async (data))

        # Then
        mock_computation.assert_called ()
        mock_executor.assert_called ()

    @patch ('main.rust_computation_wrapper', side_effect=Exception ('Computation error'))
    @patch ('main.ProcessPoolExecutor')
    def computation_error(self, mock_executor, mock_computation):
        # Given
        data = [1, 2, 3, 4]
        rust_python_integration = RustPythonIntegration ()

        # When
        with self.assertRaises (Exception) as context:
            asyncio.run (rust_python_integration.main_async (data))

        # Then
        self.assertTrue ('Computation error' in str (context.exception))

    @patch ('main.rust_computation_wrapper', return_value=1)
    @patch ('main.ProcessPoolExecutor')
    def empty_data(self, mock_executor, mock_computation):
        # Given
        data = []
        rust_python_integration = RustPythonIntegration ()

        # When
        asyncio.run (rust_python_integration.main_async (data))

        # Then
        mock_computation.assert_not_called ()
        mock_executor.assert_not_called ()


@patch ('main.rust_computation_wrapper', return_value=1)
@patch ('main.ProcessPoolExecutor')
def computation_error(self, mock_executor, mock_computation):
    # Given
    data = [1, 2, 3, 4]
    rust_python_integration = RustPythonIntegration ()

    # When
    with self.assertRaises (Exception) as context:
        asyncio.run (rust_python_integration.main_async (data))

    # Then
    self.assertTrue ('Computation error' in str (context.exception))


if __name__ == '__main__':
    unittest.main ()
