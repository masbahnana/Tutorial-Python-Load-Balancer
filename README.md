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

## Balanceando um pouco mais 

Agora vamos criar um arquivo chamado ```index.py``` (ou outro nome que voce queira). Nesse código vamos colocar a o ```getpid``` que vai nos mostrar o numero do servidor e também um "caminho" pra nossa url. 

Ah! Também vamos colocar outra porta para o nosso balanceamento. 

```
import tornado.ioloop
import tornado.web
import sys
import os

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(f"Served from {os.getpid()}")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/basic", basicRequestHandler)
    ])

    port = 8882
    if (sys.argv.__len__() > 1):
        port = sys.argv[1]

    app.listen(port)
    print(f"Application is ready and listening on port {port}")
    tornado.ioloop.IOLoop.current().start()
```

Vá até o terminal e digite 

```python3 index.py``` e no navegador voce poderá acessar ```localhost:8882/basic```

E para explorar mais vamos acessar outras portas, vá até o terminal e digite 

```python3 index.py 1111``` e depois ```python3 index.py 2222``` e também  ```python3 index.py 3333```

Voce pode tambem acessar de outros navegadores e ver que o numero do servidor mudou. Mas tambem da muito trabalho ficarmos digitando no terminal porta por porta, então vamos escrever a configuração do nosso balancer em seguida. 


## NGINX 
Pra nós não precisarmos ficar digitando porta por porta, vamos utilizar o NGINX pra fazer esse trabalho pra nós e agora vamos de fato balancear as cargas. 

### Instalação:
Pra instalar o NGINX vai depender do sistema operacional que voce está usando. Na [documentação](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) tem essa parte mais detalhada.

Depois de instalado digite no terminal ```sudo nginx```

#### Escrevendo o arquivo de configuração: 
Agora vamos abrir mais um arquivo que vou chamar de ```python.conf``` e nele vamos escrever os nossos servidores, portas e URL para o NGINX entender o que queremos.

```
upstream pythonweb{
    
    server localhost:1111;
    server localhost:2222;
    server localhost:3333;
}

server{
    listen 80;

    location /basic{
        proxy_pass "http://pythonweb/basic";
    }
}
```

Obs: a url utilizada aqui não existem, mas nao tem problema. 

### Upstream? 
Upstream define um "cluster" para o qual você pode enviar solicitações de proxy . É comumente usado para definir um cluster de servidor da web para balanceamento de carga ou um cluster de servidor de aplicativo para roteamento / balanceamento de carga.

## Configurando o NGINX
Agora precisamos configurar o NGINX para que ele encontre o nosso arquivo ```python.conf```. 

Utilize ```cd /usr/local/etc/nginx/``` pra achar os arquivos de configuração, abra o aquivo chamado ```nginx.conf.default``` (se esse arquivo não existir voce pode cria-lo, [aqui](/Tutorial-Python-Load-Balancer/nginx.conf.default) tem o exemplo). 
Nas últimas linhas tem uma linhas escrito ```include servers/*;``` abaixo dessa linha voce escreve ```include /caminho/da/pasta/com/o/arquivo/python.conf``` (por exemplo ```User/nraythz/code/pythonb/python.conf).

Obs: não mexa em mais nada do código de configuração do NGINX

Depois de terminar a configuração vá até o terminal e digite ```sudo nginx -s reload``` isso vai recarregar as configurações do NGINX e o nosso load balancer está pronto. 

Agora vá até o terminal, na pasta do seu código e digite ```python3 index.py``` e acesse nos navegadores ```localhost:8882/basic``` e a partir de agora é possível ver diferentes numeros de servers e isso significa que o nosso load balancer está funcionando.