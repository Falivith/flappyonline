<h1 align="center"> 🕹️  Flappy Bird -  Online 🕹️ </h1>

<p align="center">
Bem-vindo ao repositório do projeto Flappy Bird Online, desenvolvido como parte da disciplina de Redes de Computadores no período de 2023/1. Este projeto tem como objetivo criar uma versão online do popular jogo Flappy Bird, implementando uma arquitetura cliente-servidor para possibilitar a interação entre múltiplos jogadores.
</p>


## 📊 Relatório prático
https://docs.google.com/document/d/11mil3Rxo3aXcRY10KA4P8kUiL3-Ei9I1MVCAcj3eTX0/edit?usp=sharing


![Exemplo de GIF](https://s6.gifyu.com/images/SgLzy.gif)



## 🚀 Tecnologias/Bibliotecas 

Esse projeto foi desenvolvido com as seguintes tecnologias e bibliotecas:

- Python
- Pygame
- Sockets
- Threads
- Git
   
## 💻 Projeto

A aplicação desenvolvida representa uma reprodução do icônico jogo "Flappy Bird" com suporte para dois jogadores simultâneo, empregando uma arquitetura cliente-servidor. Nesse cenário cada jogador opera um cliente individual, e o servidor desempenha o papel crucial de intermediar a comunicação entre esses clientes. Cada jogador inicia sua própria instância do cliente, enquanto o servidor desempenha o papel de facilitador, coordenando e compartilhando informações entre os diferentes clientes. A interação entre jogadores é habilitada pelo servidor, que redireciona dados de um cliente para outro.
A troca de informações entre os jogadores é estabelecida por meio de sockets, empregando o protocolo TCP (Transmission Control Protocol). O TCP garante uma conexão confiável, assegurando a entrega ordenada e sem erros dos dados trocados. 
	Protocolo utiliza tanto Push quanto Pull. Usamos Push para enviar atualizações de posições dos jogadores, enquanto Pull é usado para receber a confirmação de prontidão dos mesmos. 

## 🔖 Executando o jogo

1. Definindo IP local
2. Abrir o codigo Config.py
3. Definir IP = "seu endereço de IP"
4. Executar codigo server.py
5. Executar 2 vezes client.py
6. Clicar em Start nos dois clientes


## 👥 Colaboração

Projeto desenvolvido por:

Ulian Gabriel Alff 
Lucas Seidy
William Rodrigues


Este projeto está aberto a contribuições e colaborações da comunidade. Se você encontrar algum problema, tiver ideias para melhorias ou quiser adicionar novos recursos, sinta-se à vontade para fazer um fork deste repositório, fazer as alterações desejadas e enviar um pull request.

Agradecemos antecipadamente a sua colaboração e estamos ansiosos para construir algo incrível juntos!
