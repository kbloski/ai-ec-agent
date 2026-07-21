import json
from di.container import Container
from infrastructure.database.db import SessionLocal
from domain.models.offers.offer import Offer
from domain.models.offers.offer_insight import OfferInsight
from domain.models.offers.offer_item import OfferItem
from domain.enums.content_status import ContentStatus
from domain.enums.offer_insight_type import OfferInsightType
from application.mappers.offer_mapper import OfferMapper


from pathlib import Path

def seed_full_offer():
    # 1. Otwieramy sesję bazy danych
    with SessionLocal() as session:
        container = Container()
        offer_assembler = container.offer_assembler()
        path_service = container.path_service()
        uploads_path = Path(path_service.UPLOADS_DEV) / "offers" / "mini_pila" 
        uploads_path = Path(path_service.UPLOADS_DEV) / "offers" / "sloik_uczuc" 

        payload = None
        with open(uploads_path / "data.json", "r", encoding="utf-8") as file:
            payload = json.load(file)

        # 2. Otwieramy blok transakcji
        with session.begin():
            try:
                new_offer = Offer(
                    name=payload["name"],
                    buying_price=payload["buying_price"],
                    details=payload["details"],
                    # target_audience=payload["target_audience"],
                    # pain_points=payload["pain_points"],
                )

                session.add(new_offer)
                session.flush()  # żeby mieć new_offer.id


                # Offer items
                offer_items = []
                for item in payload["offer_items"]:
                    offer_item = OfferItem(
                        offer_id=new_offer.id,
                        name=item["name"],
                        quantity=item["quantity"],
                        details=item["details"],
                    )

                    offer_items.append(offer_item)
                session.add_all(offer_items)

                # Offer Insights
                offer_insights = []

                for item in payload["target_audience"]:
                    offer_insight_item = OfferInsight(
                        offer_id=new_offer.id,
                        type=OfferInsightType.TARGET_AUDIENCE.value,
                        content_status=ContentStatus.APPROVED.value,
                        value=item
                    )
                    offer_insights.append(offer_insight_item)

                for item in payload["pain_points"]:
                    offer_insight_item = OfferInsight(
                        offer_id=new_offer.id,
                        type=OfferInsightType.PAIN_POINTS.value,
                        content_status=ContentStatus.APPROVED.value,
                        value=item
                    )
                    offer_insights.append(offer_insight_item)

                session.add_all(offer_insights)
            except Exception as e:
                print(f"Błąd podczas seedowania, transakcja wycofana: {e}")
                raise

        
        offer_dto = OfferMapper.to_dto(item=new_offer)
        offer_assembled = offer_assembler.assemble_dto(item=offer_dto)

        return offer_assembled