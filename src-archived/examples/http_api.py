from aiohttp import web

from asyncworker import App
from asyncworker.http.types import PathParam

app = App()


@app.http.get(["/", "/other"])
async def handler():
    return web.json_response({})


@app.http.get(["/path/{id}/accounts/{foo}"])
async def _accounts(id: PathParam[int], foo: PathParam[str]):
    _id: int = await id.unpack()
    return web.json_response({"account_id": _id})


@app.http.get(["/users/{_id}/books/{shelf}"])
async def _user_books(_id: PathParam[int], shelf: PathParam[int]):
    _id_value: int = await _id.unpack()
    shelf_id = await shelf.unpack()
    return web.json_response({"user_id": _id_value, "shelf_id": shelf_id})


app.run()
