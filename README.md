# 🤖 Totem Interativo com IA - Inovaweek 2025

## 📖 Sobre o Projeto

Este repositório contém o código-fonte de uma aplicação web interativa desenvolvida para um totem na **Inovaweek 2025**. O objetivo é engajar os participantes do evento, oferecendo uma experiência única e memorável.

A aplicação guia o usuário através de um fluxo simples: captura de uma foto, um quiz interativo e, por fim, a geração de uma imagem personalizada usando a API do **Google Gemini**. A imagem final, que estiliza o usuário em um cenário futurista de mineração, pode ser impressa na hora ou baixada via QR Code.

### ✨ Fluxo do Usuário

`Tela de Boas-Vindas` → `Captura de Foto` → `Quiz Interativo` → `Geração da Imagem com IA` → `Tela de Resultado (Download/Impressão)`

## 🚀 Principais Funcionalidades

* **Captura de Foto via Webcam:** Interface simples para o usuário tirar sua foto no totem.
* **Quiz Interativo:** Questionário personalizável que influencia o resultado final da imagem.
* **Geração de Imagem com IA:** Conecta-se à API do Google Gemini para criar uma imagem única, "vestindo" o usuário com um traje futurista sobre um dos cinco cenários pré-definidos.
* **Composição de Imagem:** Adiciona automaticamente o logo do evento e textos à imagem final.
* **QR Code para Download:** Gera um QR Code para que o usuário possa baixar facilmente sua imagem no celular.
* **Funcionalidade de Impressão:** Integração para enviar a imagem final a uma impressora conectada ao totem.

## 🛠️ Tecnologias Utilizadas

Este projeto é dividido em um front-end (a interface com o usuário) e um back-end (o cérebro da aplicação).

| Parte       | Tecnologia       | Descrição                                                          |
| :---------- | :--------------- | :----------------------------------------------------------------- |
| **Front-end** | **React** | Biblioteca JavaScript para construir a interface de usuário reativa. |
|             | **Axios** | Cliente HTTP para a comunicação entre o front-end e o back-end.      |
| **Back-end** | **Python 3.11** | Linguagem principal para a lógica do servidor.                     |
|             | **Flask** | Micro-framework web para criar a API que o front-end consome.        |
|             | **Pillow** | Biblioteca para manipulação final da imagem (adicionar logo).      |
|             | **qrcode** | Biblioteca para gerar os QR Codes.                                 |
| **API de IA** | **Google Gemini** | Serviço utilizado para a geração da imagem personalizada.            |

## ⚙️ Estrutura do Projeto
/inovaweek-totem
├── /backend
│   ├── /assets       # Imagens de fundo e logo
│   ├── /static       # Imagens finais e QR Codes gerados
│   ├── /venv         # Ambiente virtual do Python
│   ├── .env          # Arquivo para a chave da API (não versionado)
│   ├── app.py        # Servidor Flask e lógica principal
│   └── requirements.txt # Dependências do Python
│
└── /frontend
├── /public
├── /src
│   ├── /components # Componentes React (Câmera, Quiz, etc.)
│   ├── App.css
│   ├── App.js      # Componente principal do React
│   └── index.js
├── package.json    # Dependências do Node.js
└── ...

## 🚀 Começando

Siga estas instruções para rodar o projeto em um ambiente de desenvolvimento local.

### Pré-requisitos

* [Python 3.11+](https://www.python.org/)
* [Node.js e npm](https://nodejs.org/)
* Uma chave de API do Google Gemini 

### Variáveis de Ambiente

O back-end precisa de uma chave de API para se conectar ao Google Gemini.

1.  Navegue até a pasta `backend`.
2.  Crie um arquivo chamado `.env`.
3.  Dentro do `.env`, adicione a seguinte linha, substituindo pela sua chave:
    ```
    GEMINI_API_KEY=SUA_CHAVE_DE_API_AQUI
    ```

## 🏃‍♀️ Rodando a Aplicação

Você precisará de **dois terminais** abertos para rodar a aplicação completa.

**1. No primeiro terminal, inicie o Back-end:**
    ```bash
    cd backend
    .\venv\Scripts\activate
    python app.py
    ```
O servidor Flask estará rodando em http://localhost:5001

2. No segundo terminal, inicie o Front-end:

    ```bash
    cd frontend
    npm start
    ```
A aplicação React abrirá automaticamente no seu navegador em http://localhost:3000.

