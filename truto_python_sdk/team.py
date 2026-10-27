from .pagination_result import PaginationResult

class Team:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all teams with pagination support."""
        return PaginationResult(self.api_client, "team", query_params)

    def get(self, team_id: str):
        """Get a specific team by ID."""
        return self.api_client._get(f"team/{team_id}")

    def update(self, team_id: str, team_data: dict):
        """Update an existing team."""
        return self.api_client._patch(f"team/{team_id}", data=team_data)

    def invite(self, team_id: str, invite_data: dict):
        """Invite a user to a team (`name`, `email`, `role`, optional `environment`)."""
        return self.api_client._post(f"team/{team_id}/invite", data=invite_data)
