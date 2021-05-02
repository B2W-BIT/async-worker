from asyncworker import App

app = App()


@app.run_every(5)
async def every_5_seconds(myapp: App):
    print("OK")


app.run()
