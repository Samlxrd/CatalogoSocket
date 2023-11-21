## Protocolo

# Partes Envolvidas

→ Cliente: A interface de usuário onde o usuário interage com o catálogo.
→ Servidor: A parte que mantém e gerencia a base de dados do catálogo.


# Objetivos
→ Permitir que o cliente consulte, adicione, edite e exclua itens do catálogo.
→ Manter a base de dados do servidor do catálogo sincronizada com as ações do cliente. 


# Eventos relevantes do sistema

→ Evento de Adição ao catálogo:
    - Cliente solicita adição de um novo filme no catálogo.
    - Servidor recebe a solicitação e adiciona o filme ao catálogo.

→ Evento de Consulta ao catálogo:
    - Cliente solicita consulta a um item do catálogo.
    - Servidor recebe a solicitação e exibe o(s) item(ns) do catálogo.

→ Evento de Exclusão ao catálogo:
    - Cliente solicita exclusão de um item do catálogo.
    - Servidor recebe a solicitação e remove o item do catálogo.

→ Evento de Alteração ao catálogo:
    - Cliente solicita alteração no catálogo.
    - Servidor recebe a solicitação e altera o item do catálogo.

→ Evento de Erro:
    - Cliente fez alguma solicitação que o sistema identificou erro.
    - Servidor notifica o cliente sobre o problema e sua provável causa.




# Padrão de Envio do Cliente

→ Pesquisar - {nome}
→ Adicionar - {nome, tipo}
→ Favoritos - {userid}
→ Alterar - {userid}
→ Excluir - {userid}
→ X