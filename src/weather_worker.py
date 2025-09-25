from PyQt6.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from src import api


class WorkerSignals(QObject):
    """Signaux pour communiquer avec le thread principal"""

    # Signal émis quand des données sont reçues
    data_received = pyqtSignal(int, dict)  # (worker_id, data)

    # Signal émis en cas d'erreur
    error_occurred = pyqtSignal(int, str)  # (worker_id, error_message)

    # Signal émis quand le travail est terminé
    finished = pyqtSignal(int)  # (worker_id,)


class WeatherWorker(QRunnable):
    """Worker pour télécharger les données météo"""

    def __init__(self, worker_id: int, city: str) -> None:
        super().__init__()
        self.worker_id = worker_id
        self.city = city
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self) -> None:
        """Exécute le téléchargement des données"""
        try:
            data = api.fetch_weather_data(self.city)
            self.signals.data_received.emit(self.worker_id, data)

        except Exception as e:
            self.signals.error_occurred.emit(self.worker_id, str(e))
        finally:
            self.signals.finished.emit(self.worker_id)
