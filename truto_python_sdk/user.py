from .pagination_result import PaginationResult

class User:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all users with pagination support."""
        return PaginationResult(self.api_client, "user", query_params)

    def get(self, user_id: str):
        """Get a specific user by ID."""
        return self.api_client._get(f"user/{user_id}")

    def me(self):
        """Get the current user."""
        return self.api_client._get("user/me")

    def update_me(self, user_data: dict):
        """Update the current user's profile."""
        return self.api_client._patch("user/me", data=user_data)

    def update(self, user_id: str, user_data: dict):
        """Update a team member (team admins only)."""
        return self.api_client._patch(f"user/{user_id}", data=user_data)
