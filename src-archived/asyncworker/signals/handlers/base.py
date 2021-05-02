from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from asyncworker import App  # noqa: F401


class SignalHandler:
    async def startup(self, app: "App"):
        pass  # pragma: no cover

    async def shutdown(self, app: "App"):
        pass  # pragma: no cover
