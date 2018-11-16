from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from asyncworker import App


class SignalHandler:
    is_enabled: bool = True

    async def startup(self, app: 'App'):
        pass

    async def shutdown(self, app: 'App'):
        pass
