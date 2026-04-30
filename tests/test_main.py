from unittest.mock import patch

from src.bitssh.__main__ import main


class TestMain:
    def test_main_calls_run(self):
        with patch("src.bitssh.__main__.run") as mock_run:
            main()
            mock_run.assert_called_once()
