from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget

from src.api import WeatherResponse
from src.weather_worker import WeatherWorker

DEFAULT_CITIES_REQUESTED = ["Paris", "London", "New York", "Tokyo", "Sydney"]


class WeatherMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_ui()
        self.setup_thread_pool()

    def setup_thread_pool(self) -> None:
        self.thread_pool = QThreadPool()
        self.active_workers: set[int] = set()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        fetch_data_button = QPushButton("Fetch Data")
        fetch_data_button.clicked.connect(self.fetch)

        self.display_data_area = QTextEdit()
        self.display_data_area.setReadOnly(True)

        main_layout.addWidget(fetch_data_button)
        main_layout.addWidget(self.display_data_area)

    def fetch(self) -> None:
        for worker_id, city in enumerate(DEFAULT_CITIES_REQUESTED, start=1):
            worker = WeatherWorker(worker_id, city)

            worker.signals.data_received.connect(self.on_data_received)
            worker.signals.error_occurred.connect(self.on_error_occurred)
            worker.signals.finished.connect(self.on_finished)

            self.thread_pool.start(worker)
            self.active_workers.add(worker_id)

    def on_data_received(self, worker_id: int, data: WeatherResponse) -> None:
        print(f"{worker_id} succeeded")
        self.display_data_area.append(f"{data['city']}: {data['temperature']}°C, {data['humidity']}%")

    def on_error_occurred(self, worker_id: int, error_message: str) -> None:
        self.display_data_area.append(f"Error occurred from worker {worker_id}: {error_message}")

    def on_finished(self, worker_id: int) -> None:
        self.active_workers.discard(worker_id)
