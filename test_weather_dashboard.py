import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import requests

# นำเข้าฟังก์ชันที่ต้องการทดสอบ
from Weather_Dashboard import (  # type: ignore
    translate_weather,
    get_weather,
    get_city_suggestions,
    show_suggestions,
    hide_suggestions,
    show_forecast_table,
)

# -----------------------------
# ✅ Test: translate_weather()
# -----------------------------
class TestTranslateWeather(unittest.TestCase):
    def test_translate_known_weather(self):
        self.assertEqual(translate_weather("Sunny"), "แดดจัด")
        self.assertEqual(translate_weather("Partly cloudy"), "มีเมฆบางส่วน")

    def test_translate_unknown_weather(self):
        self.assertEqual(translate_weather("Hail"), "Hail")

    def test_translate_case_insensitive(self):
        self.assertEqual(translate_weather("sunny"), "แดดจัด")


# -----------------------------
# ✅ Test: get_weather()
# -----------------------------
class TestGetWeather(unittest.TestCase):
    @patch("Weather_Dashboard.requests.get")
    def test_get_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "current_condition": [{
                "temp_C": "30",
                "humidity": "60",
                "weatherDesc": [{"value": "Sunny"}]
            }],
            "weather": [{"date": "2025-10-07"}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = get_weather("Bangkok")
        self.assertIn("city", result)
        self.assertIn("temp", result)
        self.assertIn("humidity", result)
        self.assertIn("desc", result)
        self.assertIn("forecast", result)

    @patch("Weather_Dashboard.requests.get", side_effect=requests.exceptions.RequestException)
    @patch("Weather_Dashboard.messagebox.showerror")
    def test_get_weather_api_fail(self, mock_msg, mock_get):
        result = get_weather("InvalidCity")
        mock_msg.assert_called_once()
        self.assertIsNone(result)


# -----------------------------
# ✅ Test: get_city_suggestions()
# -----------------------------
class TestGetCitySuggestions(unittest.TestCase):
    @patch("Weather_Dashboard.requests.get")
    def test_get_city_suggestions_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [{"name": "Bangkok"}, {"name": "Bangsaen"}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = get_city_suggestions("Bang")
        self.assertIn("Bangkok", result)
        self.assertIn("Bangsaen", result)

    def test_get_city_suggestions_empty_query(self):
        self.assertEqual(get_city_suggestions(""), [])

    @patch("Weather_Dashboard.requests.get", side_effect=requests.exceptions.RequestException)
    def test_get_city_suggestions_api_fail(self, mock_get):
        self.assertEqual(get_city_suggestions("Bang"), [])

    @patch("Weather_Dashboard.requests.get")
    def test_get_city_suggestions_no_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        self.assertEqual(get_city_suggestions("Unknown"), [])


import unittest
import tkinter as tk
from Weather_Dashboard import show_suggestions, suggestion_window, root, city_entry  # import ของจริง

def is_display_available():
    try:
        r = tk.Tk()
        r.withdraw()
        r.destroy()
        return True
    except:
        return False

class TestSuggestionUI(unittest.TestCase):
    def setUp(self):
        # สร้าง root และ city_entry mock สำหรับ test
        self.root = tk.Tk()
        self.root.withdraw()
        self.city_entry = tk.Entry(self.root)
        self.city_entry.pack()
        # แทนที่ root และ city_entry ของโมดูล
        import Weather_Dashboard
        Weather_Dashboard.root = self.root
        Weather_Dashboard.city_entry = self.city_entry

    def tearDown(self):
        self.root.destroy()

    @unittest.skipUnless(is_display_available(), "GUI not available for tkinter")
    def test_show_suggestions_with_data(self):
        import Weather_Dashboard
        Weather_Dashboard.show_suggestions(["Bangkok", "Bangsaen"])
        self.assertIsNotNone(Weather_Dashboard.suggestion_window)



# -----------------------------
# ✅ Test: show_forecast_table()
# -----------------------------
class TestForecastTable(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.tree = tk.ttk.Treeview(self.root, columns=("วันที่", "สูงสุด", "ต่ำสุด", "สภาพอากาศ"))
        self.tree.pack()
        # แทน forecast_tree ใน Weather_Dashboard
        import Weather_Dashboard # type: ignore
        Weather_Dashboard.forecast_tree = self.tree

    def tearDown(self):
        self.root.destroy()

    def test_show_forecast_table_with_data(self):
        sample_forecast = [
            {
                "date": "2025-10-07",
                "maxtempC": "35",
                "mintempC": "25",
                "hourly": [{"weatherDesc": [{"value": "Sunny"}]}]*8
            }
        ]
        show_forecast_table(sample_forecast)
        rows = self.tree.get_children()
        self.assertTrue(len(rows) > 0)

    def test_show_forecast_table_empty(self):
        show_forecast_table([])
        rows = self.tree.get_children()
        self.assertEqual(len(rows), 0)


if __name__ == "__main__":
    unittest.main()
