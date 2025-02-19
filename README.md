![Agente de pensiones](https://general-images-bucket.s3.sa-east-1.amazonaws.com/agente_pensiones.webp)

# Agente de Pensiones - Asistente Virtual

Un asistente virtual inteligente especializado en temas previsionales, construido con FastAPI, LangChain y OpenAI.

## 🌟 Características

- Asistente virtual con conocimiento especializado en temas previsionales
- Memoria de conversación persistente con Redis
- Búsqueda de información relevante con Pinecone
- Respuestas formateadas en Markdown
- Soporte para múltiples agentes con diferentes personalidades
- Sistema de CORS configurable para seguridad

## 🛠️ Tecnologías

- Python 3.12+
- FastAPI
- LangChain & LangGraph
- OpenAI GPT
- Pinecone (Vector Store)
- Redis (Memoria de conversación)
- Uvicorn (Servidor ASGI)

## 📋 Requisitos Previos

- Python 3.12 o superior
- Redis Server
- Cuenta en Pinecone
- Claves de API para OpenAI

## 🚀 Instalación

1. Clonar el repositorio:

```bash
git clone [url-del-repositorio]
cd agente-pension
```

2. Crear y activar entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

3. Instalar dependencias:

```bash
pip install -e .
```

4. Configurar variables de entorno:

Editar .env con tus claves de API y variables de entorno.

## ⚙️ Variables de Entorno

### Crear un archivo `.env` con las siguientes variables:

### OpenAI

```env
OPENAI_API_KEY=tu-api-key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Pinecone

```env
PINECONE_API_KEY=tu-api-key
PINECONE_INDEX_NAME=nombre-del-indice
```

### Redis

```env
REDIS_URL=redis://localhost:6379/0
```

### CORS

```env
# Para múltiples dominios
CORS_ORIGINS=https://tudominio.com,https://app.tudominio.com

# O para permitir todos los subdominios
CORS_ORIGINS=https://thefullstack.digital
```

> **Nota**: Asegúrate de no compartir o commitear tu archivo `.env` con las claves reales.

## 🖥️ Uso

### Iniciar el servidor:

```bash
uvicorn main:app --reload
```

### CLI para pruebas:

```bash
python cli.py
```

## 📝 API Endpoints

### POST /chat

```json
{
"session_id": "uuid-session",
"user_message": "mensaje del usuario",
"message_type": "user",
"agent_name": "Alexandra"
}
```

## 👥 Contribución

1. Fork el proyecto
2. Crea tu Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al Branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles.

## 📚 Anexo: Fuentes de Información (RAG)

El asistente utiliza un sistema de RAG (Retrieval-Augmented Generation) que se alimenta de las siguientes fuentes oficiales y medios de comunicación verificados:

### 🏛️ Fuentes Gubernamentales

- [Previsión Social](https://previsionsocial.gob.cl)
  - Documentación oficial del sistema previsional
  - Normativas y regulaciones vigentes
  - Información sobre beneficios y trámites

### 📰 Medios de Prensa

- **Medios Nacionales**
  - La Tercera
  - El Mostrador
  - BioBioChile
  - CIPER Chile
  - Diario Financiero
  - EMOL
  - Otros medios nacionales

- **Medios Internacionales**
  - El País
  - CNN en Español

### 📺 Contenido Audiovisual

- **Canales de Noticias**
  - 24 Horas TVN Chile
  - CHV Noticias
  - Otros canales informativos verificados

> **Nota**: La información se actualiza periódicamente para mantener la base de conocimientos al día con los últimos cambios en el sistema previsional.

### 📁 Archivos de Fuentes Detalladas

El detalle completo de las fuentes utilizadas se encuentra en los siguientes archivos JSON:

- `successful_urls.json`: Contiene el listado completo de fuentes escritas (27 fuentes)
- `successful_videos.json`: Contiene el listado completo de fuentes audiovisuales (15 videos)
- `previsionsocial_pages.json`: Contiene el listado completo de fuentes del sitio web de Previsión Social (489 páginas)

Estos archivos son actualizados periódicamente y contienen metadatos como URLs, títulos y rutas de almacenamiento del contenido procesado.

> **Nota técnica**: Los archivos JSON se encuentran en la raíz del proyecto y son utilizados por el sistema RAG para recuperar información relevante durante las consultas.
