import unittest
from app import app 
from datetime import datetime

class TestStockAppInputs(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_symbol_validation(self):

        valid_symbols = ["AAPL", "GOOGL", "TSLA"]
        for symbol in valid_symbols:
            response = self.app.post('/get_stock_data', data={
                'symbol': symbol,
                'chart_type': 'line',
                'time_series': 'TIME_SERIES_DAILY',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31'
            })
            self.assertNotIn(b"Error", response.data)


        invalid_symbols = ["apple", "GOOGLE123", "A@PL"]
        for symbol in invalid_symbols:
            response = self.app.post('/get_stock_data', data={
                'symbol': symbol,
                'chart_type': 'line',
                'time_series': 'TIME_SERIES_DAILY',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31'
            })
            self.assertIn(b"Error", response.data)

    def test_chart_type_validation(self):

        valid_chart_types = ['line', 'bar']
        for chart_type in valid_chart_types:
            response = self.app.post('/get_stock_data', data={
                'symbol': 'AAPL',
                'chart_type': chart_type,
                'time_series': 'TIME_SERIES_DAILY',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31'
            })
            self.assertNotIn(b"Error", response.data)


        invalid_chart_types = ['scatter', '3']
        for chart_type in invalid_chart_types:
            response = self.app.post('/get_stock_data', data={
                'symbol': 'AAPL',
                'chart_type': chart_type,
                'time_series': 'TIME_SERIES_DAILY',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31'
            })
            self.assertIn(b"Error", response.data)

    def test_time_series_validation(self):

        valid_time_series = ['TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY', 'TIME_SERIES_MONTHLY']
        for time_series in valid_time_series:
            response = self.app.post('/get_stock_data', data={
                'symbol': 'AAPL',
                'chart_type': 'line',
                'time_series': time_series,
                'start_date': '2023-01-01',
                'end_date': '2023-12-31'
            })
            self.assertNotIn(b"Error", response.data)

        invalid_time_series = ['TIME_SERIES_YEARLY', '5']
        for time_series in invalid_time_series:
            response = self.app.post('/get_stock_data', data={
                'symbol': 'AAPL',
                'chart_type': 'line',
                'time_series': time_series,
                'start_date': '2023-01-01',
                'end_date': '2023-12-31'
            })
            self.assertIn(b"Error", response.data)

    def test_date_format_validation(self):

        response = self.app.post('/get_stock_data', data={
            'symbol': 'AAPL',
            'chart_type': 'line',
            'time_series': 'TIME_SERIES_DAILY',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        })
        self.assertNotIn(b"Error", response.data)

        response = self.app.post('/get_stock_data', data={
            'symbol': 'AAPL',
            'chart_type': 'line',
            'time_series': 'TIME_SERIES_DAILY',
            'start_date': '01-01-2023',
            'end_date': '12-31-2023'
        })
        self.assertIn(b"Error", response.data)

        response = self.app.post('/get_stock_data', data={
            'symbol': 'AAPL',
            'chart_type': 'line',
            'time_series': 'TIME_SERIES_DAILY',
            'start_date': '2023-12-31',
            'end_date': '2023-01-01'
        })
        self.assertIn(b"Error", response.data)

if __name__ == '__main__':
    unittest.main()
