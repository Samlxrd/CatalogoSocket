# Catalogo Socket

O CatalogoSocket é um software distribuído projetado para permitir que os usuários possam registrar itens, armazenando informações como nomes e tipos (filmes, animes, séries, entre outros). Além disso, os usuários têm a capacidade de adicionar itens à sua lista de favoritos para facilitar a visualização mesmos.

**Desenvolvido por: Samyr Ribeiro dos Santos**

## Requisitos Mínimos de Funcionamento:

Python:
* O software foi implementado em Python, portanto, é necessário ter o interpretador Python instalado nos ambientes onde serão executados o cliente e servidor.
* Versão: 3.10.5

Bibliotecas Utilizadas:

* socket: Facilita a implementação da comunicação via rede entre clientes e servidor.

* threading: Permite a execução simultânea de diferentes operações, foi usado principalmente para lidar separadamente com as conexões dos clientes.

* tkinter: Utilizada para a criação da interface gráfica, proporcionando uma experiência amigável aos usuários.

* json: Usado para facilitar a troca de informações estruturadas entre clientes e servidor.

* sqlite3: Essencial para a integração do banco de dados SQLite, permitindo o armazenamento persistente de informações sobre usuários, itens do catálogo e listas de favoritos.

## Motivação da Escolha do Protocolo de Transporte:

O "CatalogoSocket" lida com operações críticas de banco de dados, como o registro de itens e atualizações na lista de favoritos dos usuários. Essas operações exigem um nível de confiabilidade na entrega de dados para garantir a integridade das informações.

Dessa forma, a escolha do TCP se alinha com as necessidades de garantir que todas as transações relacionadas ao banco de dados sejam concluídas com sucesso, evitando a perda de informações relacionadas às operações dos clientes com o servidor.

## Funcionamento do Software:
* Lado do Cliente:

  `client.py` - Comunicação com o Servidor:
  * O arquivo client.py gerencia a comunicação entre o cliente e o servidor. Ele estabelece uma conexão Cliente → Servidor via socket, permitindo o envio de solicitações e o recebimento das respostas do servidor. Essa comunicação é vital para operações no catálogo.

  `interface.py` - Usabilidade Aprimorada:
  * O componente de interface gráfica fornece uma experiência amigável ao usuário. Ele apresenta opções disponíveis, recebe entradas do usuário e interage com o arquivo client.py para realizar operações desejadas. A navegação consistente simplifica a interação do usuário com o sistema.
 
* Lado do Servidor:

  `catalogo.py` - Operações no Banco de Dados:
  * Esse componente é responsável por se conectar e gerenciar as operações no banco de dados SQLite. Ele lida com a criação das tabelas, inserção de novos usuários, recuperação de dados relacionados aos itens registrados e todas as demais operações disponíveis no sistema.

  `server.py` - Gerenciamento de Conexões:
  * O arquivo server.py é crucial para o funcionamento do lado do servidor. Ele gerencia as conexões dos clientes, cria threads para lidar com várias solicitações simultâneas e roteia as requisições para as operações adequadas no arquivo catalogo.py. Garante, assim, uma resposta eficiente a todas as solicitações dos clientes.
  * Utiliza sockets para estabelecer a conexão Servidor → Cliente, permitindo a transmissão de dados pela rede.

### Executando o software:
 * Servidor: 
   * Abra um terminal ou prompt de comando no diretório onde está localizado o arquivo `server.py`;
   * Execute o seguinte comando para iniciar o servidor: `python server.py`
   * O servidor estará agora em execução, aguardando conexões de clientes.
 
 * Cliente:
   * Abra um terminal ou prompt de comando no diretório onde está localizado o arquivo `interface.py`;
   * Execute o seguinte comando para iniciar o cliente: `python interface.py`
   * Uma interface será exibida solicitando um nome de usuário. Tendo confirmado o nome de usuário, será feita a conexão do cliente com o servidor, e uma nova interface será exibida, apresentando as opções "Catálogo", "Favoritos" e "Sair". Interaja com a interface selecionando as opções desejadas para explorar o catálogo, gerenciar favoritos e realizar outras operações.
 
**(Certifique-se de que o seu ambiente atende aos [Requisitos Mínimos de Funcionamento](#requisitos-mínimos-de-funcionamento) e o servidor está com host e porta configurados corretamente.)**
 
### Fluxo Geral do Software:

 * Inicialização do Cliente:
  O cliente inicia o programa, insere o nome de usuário em um pop-up na tela e, em seguida, é exibida uma interface gráfica com as opções principais: "Catálogo", "Favoritos" e "Sair".

 * Explorando o Catálogo:
   Ao selecionar "Catálogo", uma nova tela é aberta, apresentando:
   * Uma tabela exibindo os itens cadastrados no catálogo (se existirem).
   * Uma seção permitindo a seleção de um item para favoritar, editar ou excluir.
   * Uma seção para adicionar um novo item, inserindo nome e selecionando o tipo.
   * Uma seção para buscar um item por nome ou exibir todo o catálogo novamente caso já tenha sido feita uma busca.
   * Opção de voltar para o menu principal.

* Interagindo com Itens no Catálogo:
 Se um item for selecionado na tabela, o usuário pode:
 Favoritar o item.
 Editar detalhes do item.
 Excluir o item.
 
* Adicionando Novos Itens ao Catálogo:
 Na seção de adição de novos itens, o usuário insere o nome e seleciona o tipo do item, que é então adicionado ao catálogo.

* Busca no Catálogo:
 Na seção de busca, o usuário digita um nome, e o software exibe os resultados correspondentes no catálogo.

* Explorando Favoritos:
 Ao selecionar "Favoritos", é exibida uma tabela com os itens favoritados pelo usuário.
 O usuário pode selecionar um item para remover dos favoritos.

* Pesquisa de Favoritos:
 Existe uma seção de pesquisa dentro da área de favoritos, onde o usuário pode digitar um nome e visualizar resultados correspondentes na lista de favoritos.

* Interagindo com Itens nos Favoritos:
 Ao selecionar um item na tabela de favoritos, o usuário pode remover o item da lista de favoritos.

* Encerramento do Programa:
 Ao selecionar "Sair", o programa é encerrado.

Esse fluxo geral oferece uma visão panorâmica de como os usuários interagem com o software, exploram o catálogo, gerenciam itens, e finalmente, encerram o programa. Cada opção na interface gráfica desencadeia ações específicas nos bastidores, interagindo com o lado do cliente e, eventualmente, comunicando-se com o lado do servidor para consultar ou atualizar o banco de dados conforme necessário. Os acontecimentos serão abordados mais detalhadamente abaixo, na seção [Protocolo de Camada de Aplicação](#protocolo-de-camada-de-aplicação)

## Protocolo de Camada de Aplicação:

 ### Eventos:
 O protocolo da camada de aplicação do software é composto por 10 eventos principais e 1 para tratar de excessões ou falhas em operações, esse último evento será descrito no fim da lista abaixo, o item "Mensagem enviada pelo serivdor" de cada evento, corresponde à mensagem esperada de resposta pelo servidor em caso de sucesso.
 
 * query_all: Evento que ocorre quando o cliente solicita a consulta de todos os itens cadastrados no catálogo.
   * Mensagem enviada pelo cliente: `{"action": "query_all"}`
   * Mensagem enviada pelo servidor: `{"status": "OK", "data":[]}` onde data[] contém `{'id': id_do_item, 'nome': nome_do_item, 'tipo': tipo_do_item}` para cada item encontrado.
   * Gatilho: Usuário clica no botão "Catálogo" na interface principal ou no botão "Mostrar todos" na seção pesquisar da interface do catálogo.
 
 * query_favorites: Evento acionado quando o cliente solicita a consulta de todos os itens favoritados por um usuário específico.
   * Mensagem enviada pelo cliente: `{"action": "query_favorites", "user_id": id_do_usuario}`
   * Mensagem enviada pelo servidor: `{"status": "OK", "data":[]}` onde data[] contém `{'id': id_do_item, 'nome': nome_do_item, 'tipo': tipo_do_item}` para cada item encontrado.
   * Gatilho: Usuário clica no botão "Favoritos" na interface principal ou no botão "Mostrar todos" na seção pesquisar da interface de favoritos.

 * insert_item: Evento que ocorre quando o cliente solicita a inserção de um novo item no catálogo.
   * Mensagem enviada pelo cliente: `{"action": "insert_item", "item_name": nome_do_item, "item_type": tipo_do_item}`
   * Mensagem enviada pelo servidor: `{"status": "OK"}`
   * Gatilho: Usuário clica no botão "Adicionar" na seção adicionar da interface do catálogo.
 
 * insert_favorite: Evento acionado quando o cliente solicita a adição de um item aos favoritos de um usuário.
   * Mensagem enviada pelo cliente: `{"action" : "insert_favorite", "user_id": id_do_usuario, "item_id": id_do_item}`
   * Mensagem enviada pelo servidor: `{"status": "OK"}`
   * Gatilho: Usuário clica no botão "Favoritar" na seção opções da interface do catálogo.

 * get_userid: Evento que ocorre quando o cliente solicita a obtenção do ID de um usuário com base no nome do usuário do cliente conectado.
   * Mensagem enviada pelo cliente: `{"action" : "get_userid", "user_name" : nome_do_usuario}`
   * Mensagem enviada pelo servidor: `{"status": "OK", "data":[]}` onde data[] contém `{'user_id': id}`.
   * Gatilho: Evento acionado quando o usuário é direcionado à tela principal.
 
 * search_item: Evento acionado quando o cliente solicita uma busca por itens no catálogo.
   * Mensagem enviada pelo cliente: `{"action": query, "item_name": nome_do_item}`
   * Mensagem enviada pelo servidor: `{"status": "OK", "data":[]}` onde data[] contém `{'id': id_do_item, 'nome': nome_do_item, 'tipo': tipo_do_item}` para cada item encontrado.
   * Gatilho: Usuário clica no botão "Buscar" na seção pesquisar da interface do catálogo.
 
 * search_favorite: Evento ocorre quando o cliente solicita uma busca por itens favoritos de um usuário.
   * Mensagem enviada pelo cliente: `{"action": query, "user_id": id_do_usuario, "item_name": nome_do_usuario}`
   * Mensagem enviada pelo servidor: `{"status": "OK", "data":[]}` onde data[] contém `{'id': id_do_item, 'nome': nome_do_item, 'tipo': tipo_do_item}` para cada item encontrado.
   * Gatilho: Usuário clica no botão "Buscar" na seção pesquisar da interface de favoritos.
 
 * update_item: Evento acionado quando o cliente solicita a atualização de informações de um item no catálogo.
   * Mensagem enviada pelo cliente: `{"action" : "update_item", "item_id": id, "item_name": nome, "item_type": tipo}`
   * Mensagem enviada pelo servidor: `{"status": "OK"}`
   * Gatilho: Usuário clica no botão "Editar" da seção opções da interface do catálogo, insere os novos dados do item (nome e/ou tipo) e clica em "Confirmar".
 
 * delete_item: Evento que ocorre quando o cliente solicita a exclusão de um item do catálogo.
   * Mensagem enviada pelo cliente: `{"action": "delete_item", "item_id": id}`
   * Mensagem enviada pelo servidor: `{"status": "OK"}`
   * Gatilho: Usuário clica no botão "Excluir" da seção opçoes da interface do catálogo e confirma a ação.
 
 * remove_favorite: Evento acionado quando o cliente solicita a remoção de um item dos favoritos de um usuário.
   * Mensagem enviada pelo cliente: `{"action" : "remove_favorite", "item_id": item_id}`
   * Mensagem enviada pelo servidor: `{"status": "OK"}`
   * Gatilho: Usuário clica no botão "Remover dos Favoritos" da seção opções na interface de favoritos.
 
 * Exception / Error: Corresponde a qualquer falha operacional no servidor em resposta a uma requisição do usuário.
   * Mensagem enviada pelo servidor: `{"status": "ERROR"}`
   * Tratamento: Após cada requisição do cliente, ele verifica a resposta do servidor e caso seja essa mensagem de erro, exibe na tela do usuário um pop-up informando que a operação correspondente obteve falha.
 
 ### Estados do Sistema:
 
 * Servidor:
   * Inicialização: O sistema está em processo de inicialização, nesse estado o servidor carrega configurações, estabelece conexões, e realiza outras tarefas necessárias nesse ambiente.
   * Esperando Requisições: O servidor está em estado de espera, aguardando solicitações dos clientes.
   * Processando Requisições: O servidor está ocupado processando as diversas requisições, interagindo com o banco de dados e preparando e formatando respostas.
   * Enviando Resposta: O servidor preparou a resposta para uma requisição e está no processo de envio dessa mensagem.

* Cliente:
   * Processando evento: O cliente verifica se ele foram fornecidas informações suficientes para realizar a solicitação de uma operação, como por exemplo verificando se os campos foram preenchidos (caso haja campos em um determinado evento) e formata a mensagem que será enviada ao servidor.
   * Enviando requisição: O cliente está em processo de envio de requisição ao servidor.
   * Aguardando Resposta: O cliente está aguardando a resposta após realizar um pedido (requisição) ao servidor.

 ### Mensagens:
 
 * Mensagens enviadas pelo servidor para o cliente:
   * Respostas de Sucesso `("status": "OK")`: Mensagens enviadas para indicar que a operação foi concluída com sucesso. Dependendo da operação, além do "status", o servidor pode incluir o campo "data" em sua mensagem de resposta, que contém uma lista de itens em seu conteúdo, e cada item é composto pelo seu ID, NOME e TIPO.
   * Respostas de Erro `("status": "ERROR")`: Mensagens enviadas para indicar que ocorreu um erro durante a execução da operação.
     
 * Mensagens enviadas pelo cliente para o servidor:
   * query_all: `{"action": "query_all"}`: O cliente solicita a consulta de todos os itens cadastrados no catálogo.
   * query_favorites: `{"action": "query_favorites", "user_id": id_do_usuario}`: O cliente solicita a consulta de todos os itens favoritados por um usuário específico.
   * insert_item: `{"action": "insert_item", "item_name": nome_do_item, "item_type": tipo_do_item}`: O cliente solicita a inserção de um novo item no catálogo.
   * insert_favorite: `{"action" : "insert_favorite", "user_id": id_do_usuario, "item_id": id_do_item}`: O cliente solicita a adição de um item aos favoritos de um usuário.
   * get_userid: `{"action" : "get_userid", "user_name" : nome_do_usuario}`: O cliente solicita a obtenção do ID de um usuário com base no nome do usuário conectado.
   * search_item: `{"action": query, "item_name": nome_do_item}`: O cliente solicita uma busca por itens no catálogo.
   * search_favorite: `{"action": query, "user_id": id_do_usuario, "item_name": nome_do_usuario}`: O cliente solicita uma busca por itens favoritos de um usuário.
   * update_item: `{"action" : "update_item", "item_id": id, "item_name": nome, "item_type": tipo}`: O cliente solicita a atualização de informações de um item no catálogo.
   * delete_item: `{"action": "delete_item", "item_id": id}`: O cliente solicita a exclusão de um item do catálogo.
   * remove_favorite: `{"action" : "remove_favorite", "item_id": item_id}`: O cliente solicita a remoção de um item dos favoritos de um usuário.

  Tabela de Comunicação:
  | **Cliente**   |           **Operação**              | **Servidor** |
  |  :---------:  |    :-------------------------:      | :----------: |
  |     -->       |         Requisita conexão           |              |
  |               |         Estabelece conexão          |      <--     |
  |     -->       |        Envia nome de usuário        |              |
  |               |        Retorna id do usuário        |      <--     |
  |     -->       |          msg: query_all             |              |
  |               |   OK + Itens do catálogo ou ERROR   |      <--     |
  |     -->       |    msg: query_favorites + dados     |              |
  |     -->       |   OK + Itens favoritados ou ERROR   |              |
  |     -->       |      msg: insert_item + dados       |              |
  |               |            OK ou ERROR              |      <--     |
  |     -->       |    msg: insert_favorite + dados     |              |
  |               |            OK ou ERROR              |      <--     |
  |     -->       |       msg: get_userid + dados       |              |
  |               |     OK + id do usuario ou ERROR     |      <--     |
  |     -->       |      msg: search_item + dados       |              |
  |               |   OK + itens encontrados ou ERROR   |      <--     |
  |     -->       |     msg: search_favorite + dados    |              |
  |               |   OK + itens encontrados ou ERROR   |      <--     |
  |     -->       |      msg: update_item + dados       |              |
  |               |            OK ou ERROR              |      <--     |
  |     -->       |      msg: delete_item + dados       |              |
  |               |            OK ou ERROR              |      <--     |
  |     -->       |     msg: remove_favorite + dados    |              |
  |               |            OK ou ERROR              |      <--     |

  * Dados:
    Para simplificar a tabela, dados foi generalizado. Entretanto, dados abrange todas as informações associadas às respectivas ações requisitadas, como descrito em [Eventos](#eventos) e [Mensagens](#mensagens).

 


