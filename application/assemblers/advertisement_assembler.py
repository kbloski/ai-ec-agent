from infrastructure.logging.logger import Logger
from application.dtos.advertisement.advertisement_dto import AdvertisementDto
from application.mappers.advertisement_scene_mapper import AdvertisementSceneMapper
from application.mappers.scene_mapper import SceneMapper
from application.mappers.advertisement_visualization_mapper import (
    AdvertisementVisualizationMapper,
)
from application.mappers.advertisement_objection_mapper import AdvertisementObjectionMapper
from infrastructure.repositories.advertisement_scenes_repository import (
    AdvertisementScenesRepository,
)
from infrastructure.repositories.scenes_repository import ScenesRepository
from infrastructure.repositories.advertisement_visualizations_repository import (
    AdvertisementVisualizationsRepository,
)
from infrastructure.repositories.advertisement_objections_repository import (
    AdvertisementObjectionsRepository,
)


class AdvertisementAssembler:
    logger: Logger
    advertisement_scenes_repository: AdvertisementScenesRepository
    scenes_repository: ScenesRepository
    advertisement_visualizations_repository: AdvertisementVisualizationsRepository
    advertisement_objections_repository: AdvertisementObjectionsRepository

    def __init__(
        self,
        logger: Logger,
        advertisement_scenes_repository: AdvertisementScenesRepository,
        scenes_repository: ScenesRepository,
        advertisement_visualizations_repository: AdvertisementVisualizationsRepository,
        advertisement_objections_repository: AdvertisementObjectionsRepository,
    ):
        self.logger = logger
        self.advertisement_scenes_repository = advertisement_scenes_repository
        self.scenes_repository = scenes_repository
        self.advertisement_visualizations_repository = advertisement_visualizations_repository
        self.advertisement_objections_repository = advertisement_objections_repository

    def assemble_dto(self, item: AdvertisementDto) -> AdvertisementDto:
        advertisement_scenes_db = self.advertisement_scenes_repository.find_for_advertisement(
            advertisement_id=item.id
        )
        advertisement_scene_dtos = [
            AdvertisementSceneMapper.to_dto(i) for i in advertisement_scenes_db
        ]

        for advertisement_scene_dto in advertisement_scene_dtos:
            scene_db = self.scenes_repository.get_by_id(id=advertisement_scene_dto.scene_id)
            if scene_db is not None:
                advertisement_scene_dto.scene = SceneMapper.to_dto(scene_db)

        item.scenes = advertisement_scene_dtos

        visualizations_db = self.advertisement_visualizations_repository.find_for_advertisement(
            advertisement_id=item.id
        )
        item.visualizations = [
            AdvertisementVisualizationMapper.to_dto(i) for i in visualizations_db
        ]

        objections_db = self.advertisement_objections_repository.find_for_advertisement(
            advertisement_id=item.id
        )
        item.objections = [AdvertisementObjectionMapper.to_dto(i) for i in objections_db]

        return item
