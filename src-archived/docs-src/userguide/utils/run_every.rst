Rodando uma função em um intervalo fixo de tempo
===================================================


O objeto :ref:`App <asyncworker-app>` posui um método utilitátio que permite que um função seja rodada de tempos em tempos. Basta anotar essa função com o decorator `@app.run_every` e ela será chamada nesse intervalo de tempo.

.. code-block:: python

  from asyncworker import App

  app = App()


  @app.run_every(5)
  async def every_5_seconds(myapp: App):
      print("OK")


  app.run()
