from typing import Optional, List, Dict, Any

from common.mixins.json_serializable import JSONSerializable


class OfferStrategyDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        brand_marketing_id: int,
        marketing_strategy_id: int,
        offer_name: Optional[str],
        offer_positioning: Optional[str],
        core_value_proposition: Optional[str],
        main_customer_problem: Optional[str],
        solution_mechanism: Optional[str],
        primary_benefit: Optional[str],
        secondary_benefits: Optional[List[str]],
        functional_benefits: Optional[List[str]],
        emotional_benefits: Optional[List[str]],
        offer_structure: Optional[Dict[str, Any]],
        value_stack: Optional[List[Any]],
        risk_reversal: Optional[List[str]],
        trust_elements: Optional[List[str]],
        pricing_strategy: Optional[str],
        urgency_strategy: Optional[str],
        customer_objection_handling: Optional[List[str]],
        competitive_difference: Optional[str],
        conversion_levers: Optional[List[str]],
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.brand_marketing_id = brand_marketing_id
        self.marketing_strategy_id = marketing_strategy_id
        self.offer_name = offer_name
        self.offer_positioning = offer_positioning
        self.core_value_proposition = core_value_proposition
        self.main_customer_problem = main_customer_problem
        self.solution_mechanism = solution_mechanism
        self.primary_benefit = primary_benefit
        self.secondary_benefits = secondary_benefits
        self.functional_benefits = functional_benefits
        self.emotional_benefits = emotional_benefits
        self.offer_structure = offer_structure
        self.value_stack = value_stack
        self.risk_reversal = risk_reversal
        self.trust_elements = trust_elements
        self.pricing_strategy = pricing_strategy
        self.urgency_strategy = urgency_strategy
        self.customer_objection_handling = customer_objection_handling
        self.competitive_difference = competitive_difference
        self.conversion_levers = conversion_levers

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "brand_marketing_id": self.brand_marketing_id,
            "marketing_strategy_id": self.marketing_strategy_id,
            "offer_name": self.offer_name,
            "offer_positioning": self.offer_positioning,
            "core_value_proposition": self.core_value_proposition,
            "main_customer_problem": self.main_customer_problem,
            "solution_mechanism": self.solution_mechanism,
            "primary_benefit": self.primary_benefit,
            "secondary_benefits": self.secondary_benefits,
            "functional_benefits": self.functional_benefits,
            "emotional_benefits": self.emotional_benefits,
            "offer_structure": self.offer_structure,
            "value_stack": self.value_stack,
            "risk_reversal": self.risk_reversal,
            "trust_elements": self.trust_elements,
            "pricing_strategy": self.pricing_strategy,
            "urgency_strategy": self.urgency_strategy,
            "customer_objection_handling": self.customer_objection_handling,
            "competitive_difference": self.competitive_difference,
            "conversion_levers": self.conversion_levers,
        }

        return {k: v for k, v in data.items() if k not in exclude}
