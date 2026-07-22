from typing import Optional, List, Dict, Any

from common.mixins.json_serializable import JSONSerializable


class MarketingStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        brand_marketing_id: int,
        marketing_objective: Optional[str],
        growth_strategy: Optional[str],
        primary_audience: Optional[List[str]],
        secondary_audience: Optional[List[str]],
        audience_prioritization: Optional[List[Dict[str, Any]]],
        customer_journey: Optional[Dict[str, Any]],
        marketing_channels: Optional[List[Dict[str, Any]]],
        acquisition_strategy: Optional[List[str]],
        trust_building_strategy: Optional[List[str]],
        content_strategy: Optional[Dict[str, Any]],
        community_strategy: Optional[List[str]],
        creator_influencer_strategy: Optional[List[str]],
        campaign_directions: Optional[List[Dict[str, Any]]],
        conversion_strategy: Optional[List[str]],
        retention_strategy: Optional[List[str]],
        marketing_experiments: Optional[List[Dict[str, Any]]],
        marketing_kpis: Optional[List[str]],
    ):
        self.id = id
        self.brand_marketing_id = brand_marketing_id
        self.marketing_objective = marketing_objective
        self.growth_strategy = growth_strategy
        self.primary_audience = primary_audience
        self.secondary_audience = secondary_audience
        self.audience_prioritization = audience_prioritization
        self.customer_journey = customer_journey
        self.marketing_channels = marketing_channels
        self.acquisition_strategy = acquisition_strategy
        self.trust_building_strategy = trust_building_strategy
        self.content_strategy = content_strategy
        self.community_strategy = community_strategy
        self.creator_influencer_strategy = creator_influencer_strategy
        self.campaign_directions = campaign_directions
        self.conversion_strategy = conversion_strategy
        self.retention_strategy = retention_strategy
        self.marketing_experiments = marketing_experiments
        self.marketing_kpis = marketing_kpis

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "brand_marketing_id": self.brand_marketing_id,
            "marketing_objective": self.marketing_objective,
            "growth_strategy": self.growth_strategy,
            "primary_audience": self.primary_audience,
            "secondary_audience": self.secondary_audience,
            "audience_prioritization": self.audience_prioritization,
            "customer_journey": self.customer_journey,
            "marketing_channels": self.marketing_channels,
            "acquisition_strategy": self.acquisition_strategy,
            "trust_building_strategy": self.trust_building_strategy,
            "content_strategy": self.content_strategy,
            "community_strategy": self.community_strategy,
            "creator_influencer_strategy": self.creator_influencer_strategy,
            "campaign_directions": self.campaign_directions,
            "conversion_strategy": self.conversion_strategy,
            "retention_strategy": self.retention_strategy,
            "marketing_experiments": self.marketing_experiments,
            "marketing_kpis": self.marketing_kpis,
        }

        return {k: v for k, v in data.items() if k not in exclude}
