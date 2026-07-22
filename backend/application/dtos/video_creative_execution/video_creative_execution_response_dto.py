from typing import Optional, List

from common.mixins.json_serializable import JSONSerializable


class VideoCreativeExecutionDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        ad_execution_id: int,
        duration_seconds: Optional[int],
        hook_strategy: Optional[dict],
        structure: Optional[List[dict]],
        scenes: Optional[List[dict]],
        asset_requirements: Optional[List[str]],
        production_notes: Optional[dict],
        cta: Optional[dict],
    ):
        self.id = id
        self.ad_execution_id = ad_execution_id
        self.duration_seconds = duration_seconds
        self.hook_strategy = hook_strategy
        self.structure = structure
        self.scenes = scenes
        self.asset_requirements = asset_requirements
        self.production_notes = production_notes
        self.cta = cta

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "ad_execution_id": self.ad_execution_id,
            "duration_seconds": self.duration_seconds,
            "hook_strategy": self.hook_strategy,
            "structure": self.structure,
            "scenes": self.scenes,
            "asset_requirements": self.asset_requirements,
            "production_notes": self.production_notes,
            "cta": self.cta,
        }

        return {k: v for k, v in data.items() if k not in exclude}
