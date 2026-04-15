from typing import Annotated

from fastapi import Depends

from src.routers.dependencies.inventory import get_inventory_manager
from src.routers.dependencies.patron import get_patron_manager
from src.services.inventory import InventoryManager
from src.services.patron import PatronManager
from src.services.library import Library


def get_library(
    inventory: Annotated[InventoryManager, Depends(get_inventory_manager)],
    patrons: Annotated[PatronManager, Depends(get_patron_manager)],
) -> Library:
    return Library(inventory=inventory, patrons=patrons)
