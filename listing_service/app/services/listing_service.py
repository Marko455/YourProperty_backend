import uuid
from app.db.dynamodb import properties_table

class ListingService:

    @staticmethod
    def create(data: dict, owner_id: str):
        property_id = str(uuid.uuid4())

        item = {
            "PK": f"PROPERTY#{property_id}",
            "SK": "METADATA",
            "property_id": property_id,
            "owner_id": owner_id,
            **data,
        }

        properties_table.put_item(Item=item)
        return item

    @staticmethod
    def get(property_id: str):
        response = properties_table.get_item(
            Key={
                "PK": f"PROPERTY#{property_id}",
                "SK": "METADATA",
            }
        )
        return response.get("Item")

    @staticmethod
    def list_by_city(city: str):
        response = properties_table.query(
            IndexName="city-index",
            KeyConditionExpression="city = :city",
            ExpressionAttributeValues={":city": city},
        )
        return response.get("Items", [])

    @staticmethod
    def update(property_id: str, owner_id: str, data: dict):
        item = ListingService.get(property_id)
        if not item or item["owner_id"] != owner_id:
            raise PermissionError()

        updates = []
        values = {}

        for k, v in data.items():
            updates.append(f"{k} = :{k}")
            values[f":{k}"] = v

        properties_table.update_item(
            Key={
                "PK": f"PROPERTY#{property_id}",
                "SK": "METADATA",
            },
            UpdateExpression="SET " + ", ".join(updates),
            ExpressionAttributeValues=values,
        )

    @staticmethod
    def delete(property_id: str, owner_id: str):
        item = ListingService.get(property_id)
        if not item or item["owner_id"] != owner_id:
            raise PermissionError()

        properties_table.delete_item(
            Key={
                "PK": f"PROPERTY#{property_id}",
                "SK": "METADATA",
            }
        )
