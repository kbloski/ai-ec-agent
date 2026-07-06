from di.container import Container
from application.mappers.offer_mapper import OfferMapper
from application.mappers.offer_item_mapper import OfferItemMapper

def analyze_offer_handler(id : int):
    container = Container()
    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()
    
    offer = offers_repository.get_by_id(  id = id )
    offer_items = offer_items_repository.get_by_offer_id( offer_id=id)

    if not offer:
        return None


    return {
        "status" : True
    }
        

