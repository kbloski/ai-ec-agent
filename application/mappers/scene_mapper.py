from domain.models.advertisement.scene import Scene
from application.dtos.advertisement.scene_dto import SceneDto


class SceneMapper:

    @staticmethod
    def to_dto(item: Scene) -> SceneDto:
        return SceneDto(
            id=item.id,
            type=item.type,
            description=item.description,
            duration_seconds=item.duration_seconds,
        )
