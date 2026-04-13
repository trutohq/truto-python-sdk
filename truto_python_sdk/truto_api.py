import aiohttp

from .dict_to_query_string import dict_to_query_string
from .alarm import Alarm
from .api_token import ApiToken
from .batch_request import BatchRequest
from .category import Category
from .custom_api import CustomApi
from .daemon import Daemon
from .daemon_job import DaemonJob
from .daemon_job_cron_trigger import DaemonJobCronTrigger
from .daemon_job_run import DaemonJobRun
from .datastore import Datastore
from .documentation import Documentation
from .environment import Environment
from .environment_integration import EnvironmentIntegration
from .environment_integration_webhook import EnvironmentIntegrationWebhook
from .integrated_account import IntegratedAccount
from .integrated_account_webhook import IntegratedAccountWebhook
from .integration import Integration
from .link_token import LinkToken
from .log import Log
from .mcp import Mcp
from .proxy_api import ProxyApi
from .sandbox_integrated_account import SandboxIntegratedAccount
from .static_gate import StaticGate
from .sync_job import SyncJob
from .sync_job_cron_trigger import SyncJobCronTrigger
from .sync_job_run import SyncJobRun
from .team import Team
from .unified_api import UnifiedApi
from .user import User
from .unified_model import UnifiedModel
from .environment_unified_model import EnvironmentUnifiedModel
from .webhook import Webhook
from .workflow import Workflow
from .workflow_run import WorkflowRun


class TrutoApi:
    def __init__(self, token: str, base_url: str = 'https://api.truto.one'):
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.users = User(self)
        self.teams = Team(self)
        self.api_tokens = ApiToken(self)
        self.environments = Environment(self)
        self.categories = Category(self)
        self.link_tokens = LinkToken(self)
        self.integrated_accounts = IntegratedAccount(self)
        self.sandbox_integrated_accounts = SandboxIntegratedAccount(self)
        self.integrations = Integration(self)
        self.environment_integrations = EnvironmentIntegration(self)
        self.environment_integration_webhooks = EnvironmentIntegrationWebhook(self)
        self.integrated_account_webhooks = IntegratedAccountWebhook(self)
        self.unified_models = UnifiedModel(self)
        self.environment_unified_models = EnvironmentUnifiedModel(self)
        self.sync_jobs = SyncJob(self)
        self.sync_job_runs = SyncJobRun(self)
        self.sync_job_cron_triggers = SyncJobCronTrigger(self)
        self.daemons = Daemon(self)
        self.daemon_jobs = DaemonJob(self)
        self.daemon_job_runs = DaemonJobRun(self)
        self.daemon_job_cron_triggers = DaemonJobCronTrigger(self)
        self.datastores = Datastore(self)
        self.alarms = Alarm(self)
        self.workflows = Workflow(self)
        self.workflow_runs = WorkflowRun(self)
        self.documentations = Documentation(self)
        self.logs = Log(self)
        self.static_gates = StaticGate(self)
        self.webhooks = Webhook(self)
        self.batch_requests = BatchRequest(self)
        self.mcp = Mcp(self)
        self.custom_api = CustomApi(self)
        self.unified_api = UnifiedApi(self)
        self.proxy_api = ProxyApi(self)

    async def _process_response(self, response):
        # Get the Content-Type header
        content_type = response.headers.get('Content-Type', '').lower()

        if 'json' in content_type:
            # If it's a JSON-like content type (application/json, text/json, etc.)
            return await response.json()
        elif content_type.startswith('text/'):
            # If it's any kind of text (e.g., text/plain, text/html)
            return await response.text()
        else:
            # For everything else (binary data, unknown types)
            return await response.read()

    async def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        query_string = dict_to_query_string(params) if params else ""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}?{query_string}", headers=self.headers) as response:
                response.raise_for_status()
                return await self._process_response(response)

    async def _post(self, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        query_string = dict_to_query_string(params) if params else ""
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{url}?{query_string}", headers=self.headers, json=data) as response:
                response.raise_for_status()
                return await self._process_response(response)

    async def _patch(self, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        query_string = dict_to_query_string(params) if params else ""
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{url}?{query_string}", headers=self.headers, json=data) as response:
                response.raise_for_status()
                return await self._process_response(response)

    async def _put(self, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        query_string = dict_to_query_string(params) if params else ""
        async with aiohttp.ClientSession() as session:
            async with session.put(f"{url}?{query_string}", headers=self.headers, json=data) as response:
                response.raise_for_status()
                return await self._process_response(response)

    async def _delete(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        query_string = dict_to_query_string(params) if params else ""
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{url}?{query_string}", headers=self.headers) as response:
                response.raise_for_status()
                return await self._process_response(response)

    async def ping(self):
        return await self._get("ping")