from domain.models.visualizations.vusualization import Visualization
from application.dtos.visualizations.visualization_dto import VisualizationDto


class VisualizationMapper:

    @staticmethod
    def to_dto(item: Visualization) -> VisualizationDto:
        return VisualizationDto(
            id=item.id,
            format=item.format,
            name=item.name,
            description=item.description,
        )
