from typing import override

from PyQt6.QtCore import QPointF, QSize
from PyQt6.QtGui import QColor, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QWidget

DEFAULT_CITIES: list[str] = ["Paris", "Lyon", "Marseille"]
DEFAULT_TEMPERATURES: list[float] = [20, 25, 22]


class ChartWidget(QWidget):
    def __init__(self, cities: list[str], temperatures: list[float]) -> None:
        super().__init__()

        self.cities = cities
        self.temperatures = temperatures
        self.setMinimumSize(400, 300)

    @override
    def sizeHint(self) -> QSize:
        return QSize(400, 300)

    def update_chart(self, cities: list[str], temperatures: list[float]) -> None:
        """Met à jour les données du graphique et redessine"""
        self.cities = cities
        self.temperatures = temperatures
        self.update()  # Déclenche un repaint

    @override
    def paintEvent(self, event: QPaintEvent | None = None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Obtenir les dimensions du widget
        width = self.width()
        height = self.height()

        # Définir les marges
        margin = 50
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin

        # Dessiner le fond du graphique
        painter.fillRect(margin, margin, chart_width, chart_height, QColor(240, 248, 255))

        # Calculer les positions des points
        # Répartir les points sur la largeur du graphique
        x_positions = [margin + chart_width * 0.2, margin + chart_width * 0.5, margin + chart_width * 0.8]

        # Normaliser les températures pour l'affichage (inverser l'axe Y)
        min_temp = min(self.temperatures)
        max_temp = max(self.temperatures)
        temp_range = max_temp - min_temp if max_temp != min_temp else 1

        y_positions = []
        for temp in self.temperatures:
            # Normaliser entre 0 et 1, puis inverser et adapter à la hauteur
            normalized = (temp - min_temp) / temp_range
            y = margin + chart_height * (1 - normalized * 0.8)  # 0.8 pour laisser de la marge
            y_positions.append(y)

        # Créer les points
        point1 = QPointF(x_positions[0], y_positions[0])
        point2 = QPointF(x_positions[1], y_positions[1])
        point3 = QPointF(x_positions[2], y_positions[2])

        # Dessiner les lignes
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawLine(point1, point2)
        painter.drawLine(point2, point3)

        # Dessiner les points
        painter.setPen(QPen(QColor(0, 0, 255), 2))
        painter.drawEllipse(point1, 8, 8)
        painter.drawEllipse(point2, 8, 8)
        painter.drawEllipse(point3, 8, 8)

        # Dessiner les étiquettes
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawText(point1 + QPointF(10, -10), f"{self.cities[0]} ({self.temperatures[0]}°C)")
        painter.drawText(point2 + QPointF(10, -10), f"{self.cities[1]} ({self.temperatures[1]}°C)")
        painter.drawText(point3 + QPointF(10, -10), f"{self.cities[2]} ({self.temperatures[2]}°C)")
