from infrastructure.database.db import SessionLocal
from domain.models.offers.offer import Offer
from domain.models.offers.offer_item import OfferItem
from di.container import Container
import json
from pathlib import Path

def seed_full_offer():
    # 1. Otwieramy sesję bazy danych
    with SessionLocal() as session:
        container = Container()
        path_service = container.path_service()
        uploads_path = Path(path_service.UPLOADS_DEV) / "offers" / "mini_pila" 

        payload = None
        with open(uploads_path / "data.json", "r", encoding="utf-8") as file:
            payload = json.load(file)

        # 2. Otwieramy blok transakcji
        with session.begin():
            try:
                new_offer = Offer(
                    name=payload["name"],
                    buying_price=payload["buying_price"],
                    description=payload["description"],
                    target_audience=payload["target_audience"],
                    pain_points=payload["pain_points"],
                )

                session.add(new_offer)
                session.flush()  # żeby mieć new_offer.id

                offer_items = []
                for item in payload["offer_items"]:
                    offer_item = OfferItem(
                        offer_id=new_offer.id,
                        name=item["name"],
                        quantity=item["quantity"],
                        details=item["details"],
                    )

                    offer_items.append(offer_item)

                # 👇 TO JEST BRAKUJĄCY KROK
                session.add_all(offer_items)
            except Exception as e:
                print(f"Błąd podczas seedowania, transakcja wycofana: {e}")
                raise

        # Kiedy kod wyjdzie poza blok `with session.begin():`, automatycznie wykonał się COMMIT.

        return {
            "success" : True
        }