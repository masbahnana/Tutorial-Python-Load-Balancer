# Tutorial-Python-Load-Balancer
Tutorial de Load Balancer utilizando Python
Vamos fazer um balanceamento de carga bem fácil e simples utilizando uma biblioteca do Python chamada Tornado. 

## Tornado
Tornado é uma estrutura da web Python e biblioteca de rede assíncrona, desenvolvida originalmente em FriendFeed . Usando E / S de rede sem bloqueio, o Tornado pode escalar para dezenas de milhares de conexões abertas, tornando-o ideal para pesquisas longas , WebSockets e outros aplicativos que requerem uma conexão de longa duração para cada usuário.
Saiba mais na [documentação](https://www.tornadoweb.org/en/stable/).

Pra instalar o Tornado é bem simples, vamos utilizar o ```pip3```:

```pip3 install tornado``` 

### Hello World

Vamos fazer o nosso primeiro aplicativo, crie uma pasta chama ```HelloWorld.py``` e coloque o seguinte código. 

```
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
````

Depois vá até o seu terminal e digite

```python3 HelloWorld.py``` e em seguida acesse no navegador a url ```localhost:8888```

