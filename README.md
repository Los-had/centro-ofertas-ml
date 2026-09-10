# Central de Ofertas ML

Sistema automatizado de monitoramento, análise e divulgação de ofertas do Mercado Livre.

O objetivo do projeto é criar uma central de ofertas capaz de encontrar produtos realmente baratos, analisar o histórico de preços, calcular a qualidade de cada oportunidade e posteriormente divulgar automaticamente as melhores ofertas através de canais como Telegram, WhatsApp e Instagram.

A ideia não é simplesmente copiar o percentual de desconto mostrado pelo Mercado Livre.

O sistema deverá tentar responder:

> "Esse produto está realmente barato agora?"

Para isso, serão armazenados preços históricos e diversos dados do produto, permitindo comparar o preço atual com o comportamento anterior daquele produto.

---

# Índice

- [Objetivo](#objetivo)
- [Como o sistema funcionará](#como-o-sistema-funcionará)
- [Funcionalidades planejadas](#funcionalidades-planejadas)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Estado atual](#estado-atual)
- [Instalação no Linux Mint](#instalação-no-linux-mint)
- [Executando o projeto](#executando-o-projeto)
- [Banco de dados](#banco-de-dados)
- [API](#api)
- [Deal Score](#deal-score)
- [Dados do produto](#dados-do-produto)
- [Integração com Mercado Livre](#integração-com-mercado-livre)
- [Sistema de afiliados](#sistema-de-afiliados)
- [Publicação automática](#publicação-automática)
- [Instagram e anúncios](#instagram-e-anúncios)
- [Analytics](#analytics)
- [Segurança](#segurança)
- [Testes](#testes)
- [Git e GitHub](#git-e-github)
- [Roadmap](#roadmap)
- [Princípios do projeto](#princípios-do-projeto)

---

# Objetivo

A Central de Ofertas ML será uma plataforma para encontrar, filtrar e divulgar ofertas do Mercado Livre.

O fluxo final pretendido é aproximadamente:

```text
                    MERCADO LIVRE
                         │
                         ▼
                  API / Dados
                         │
                         ▼
                ┌─────────────────┐
                │ Banco de dados  │
                │    SQLite       │
                └────────┬────────┘
                         │
                         ▼
                 Histórico de preço
                         │
                         ▼
                  Análise do produto
                         │
                         ▼
                   DEAL SCORE
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Excelente    Boa        Fraca
            oferta     oferta      oferta
              │          │
              ▼          ▼
          Publicar    Revisar    Ignorar
                         │
                         ▼
              Link de afiliado
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Telegram        WhatsApp      Instagram
                         │
                         ▼
                    Usuários
                         │
                         ▼
                  Cliques / vendas
                         │
                         ▼
                    Comissão
                         │
                         ▼
                  Receita / lucro
