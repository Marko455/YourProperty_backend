from app.db.dynamodb import users_table

class UserService:

    @staticmethod
    def get_profile(user_id: str):
        response = users_table.get_item(
            Key={
                "PK": f"USER#{user_id}",
                "SK": "PROFILE",
            }
        )
        return response.get("Item")

    @staticmethod
    def update_profile(user_id: str, data: dict):
        update_expression = []
        expression_values = {}

        for key, value in data.items():
            update_expression.append(f"{key} = :{key}")
            expression_values[f":{key}"] = value

        if not update_expression:
            return

        users_table.update_item(
            Key={
                "PK": f"USER#{user_id}",
                "SK": "PROFILE",
            },
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_values,
        )
