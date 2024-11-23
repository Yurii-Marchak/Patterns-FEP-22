from item import Small, Heavy, Refrigerated, Liquid

class ItemFactory:
    @staticmethod
    def create_item(item_type: str, id: int, weight: float, count: int, container_id: int):
        if item_type == "small":
            return Small(id, weight, count, container_id)
        elif item_type == "heavy":
            return Heavy(id, weight, count, container_id)
        elif item_type == "refrigerated":
            return Refrigerated(id, weight, count, container_id)
        elif item_type == "liquid":
            return Liquid(id, weight, count, container_id)
        else:
            raise ValueError(f"Unknown item type: {item_type}")
