import sys

from PyQt6.QtWidgets import QApplication

from src.main_window import WeatherMainWindow


def main() -> int:
    app = QApplication(sys.argv)

    window = WeatherMainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
