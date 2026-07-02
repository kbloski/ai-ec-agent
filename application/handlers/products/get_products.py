from di.container import Container

def get_products(page : int):
    container = Container()
    product_repository = container.product_repository()
    result = product_repository.search(
        page=page
    )
    return result
        

