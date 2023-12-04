#Catalogo Socket

### Propósito do software:

O "CatalogoSocket" é um software distribuído projetado para permitir o registro de itens, armazenando informações como nomes e tipos (filmes, animes, séries, entre outros). Além disso, os usuários têm a capacidade de adicionar itens à sua lista de favoritos para facilitar a visualização.

### Motivação da Escolha do Protocolo de Transporte:

O "CatalogoSocket" lida com operações críticas de banco de dados, como o registro de itens e atualizações na lista de favoritos dos usuários. Essas operações exigem um nível de confiabilidade na entrega de dados para garantir a integridade das informações.

Dessa forma, a escolha do TCP se alinha com as necessidades de garantir que todas as transações relacionadas ao banco de dados sejam concluídas com sucesso, evitando a perda de informações relacionadas às operações dos clientes com o servidor.

### Requisitos Mínimos de Funcionamento:

Python:
- O software foi implementado em Python 3.10.5, portanto, é necessário ter o interpretador Python instalado nos ambientes onde serão executados o cliente e servidor.

Bibliotecas Utilizadas:

- socket: Facilita a implementação da comunicação via rede entre clientes e servidor.

- threading: Permite a execução simultânea de diferentes operações, foi usado principalmente para lidar separadamente com as conexões dos clientes.

- tkinter: Utilizada para a criação da interface gráfica, proporcionando uma experiência amigável aos usuários.

- json: Usado para facilitar a troca de informações estruturadas entre clientes e servidor.

- sqlite3: Essencial para a integração do banco de dados SQLite, permitindo o armazenamento persistente de informações sobre usuários, itens do catálogo e listas de favoritos.

### Funcionamento do Software:
* Lado do Cliente:

 `client.py` - Comunicação com o Servidor:
 - O arquivo client.py gerencia a comunicação entre o cliente e o servidor. Ele estabelece uma conexão via socket, envia solicitações ao servidor e recebe as respostas correspondentes. Essa comunicação é vital para operações no catálogo.

 `interface.py` - Usabilidade Aprimorada:
 - O componente de interface gráfica fornece uma experiência amigável ao usuário. Ele apresenta opções disponíveis, recebe entradas do usuário e interage com o arquivo client.py para realizar operações desejadas. A navegação consistente simplifica a interação do usuário com o sistema.
 
* Lado do Servidor:

 `catalogo.py` - Operações no Banco de Dados:
 - Esse componente é responsável por se conectar e gerenciar as operações no banco de dados SQLite. Ele lida com a criação das tabelas, inserção de novos usuários, recuperação de dados relacionados aos itens registrados e todas as demais operações disponíveis do sistema.

 `server.py` - Gerenciamento de Conexões:
 - O arquivo server.py é crucial para o funcionamento do lado do servidor. Ele gerencia as conexões dos clientes, cria threads para lidar com várias solicitações simultâneas e roteia as requisições para as operações adequadas no arquivo catalogo.py. Garante, assim, uma resposta eficiente a todas as solicitações dos clientes.

#### Executando o software:
 * Servidor: 
  * Abra um terminal ou prompt de comando no diretório onde está localizado o arquivo `server.py`;
  * Execute o seguinte comando para iniciar o servidor: `python server.py`
  * O servidor estará agora em execução, aguardando conexões de clientes.
 
 * Cliente:
  * Abra um terminal ou prompt de comando no diretório onde está localizado o arquivo `interface.py`;
  * Execute o seguinte comando para iniciar o cliente: `python interface.py`
  * Uma interface será exibida solicitando um nome de usuário. Tendo confirmado o nome de usuário, será feita a conexão do cliente com o servidor, e uma nova interface será exibida, com as opções disponíveis para o usuário acessar no sistema.
 
**(Certifique-se de que o seu ambiente atende aos Requisitos Mínimos de Funcionamento e o servidor está com host e porta configurados corretamente.)**
 
#### Fluxo Geral do Software:
 
