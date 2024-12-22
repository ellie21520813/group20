<a name="readme-top"></a>


<!-- ABOUT THE PROJECT -->
## About The Project


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![React][React.js]][React-url]
* [![FastAPI][FastAPI-logo]][FastAPI-url]
* [![Postgresql][Postgresql-logo]][Postgresql-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* docker

### Installation

_Below is how you can installing and setting up app._

1. Clone the repo
   ```sh
   git clone https://github.com/nvbao45/MOD-Edge.git
   ```
2. Add `.env` file in `MODE-Edge` folder
   ```
   # Postgres config
    POSTGRES_VERSION=latest
    POSTGRES_USER=<postgres_username>
    POSTGRES_PASSWORD=<postgres_password>

    # Redis config
    REDIS_PASSWORD=<redis password>

    # Rabbitmq config
    RABBITMQ_USER=<rabbitmq_user>
    RABBITMQ_PASS=<rabbitmq_password>

    # Config host
    HOST_IP=192.168.31.76

    # Services Port
    AUTH_PORT=8000
    TASK_PORT=8001
    USER_PORT=8002
    CAST_PORT=8003
    MOVI_PORT=8004
    FILE_PORT=8005
    LSTM_PORT=8006
    DEVI_PORT=8007
    AI_PORT=8008

    # Database Port
    DEV_DB_PORT=7000
   ```
4. In `ui` folder add `.env` file
    ```
    REACT_APP_BE=192.168.31.76 
    REACT_APP_BASE_URL=http://192.168.31.76/
    REACT_APP_API_URL=http://192.168.31.76/api
    REACT_APP_ASSETS_BUCKET=https://lightence-assets.s3.amazonaws.com
    ESLINT_NO_DEV_ERRORS=true
    TSC_COMPILE_ON_ERROR=true
    REACT_APP_DEVICE_COMMAND_TOKEN=d1f49e16-6c73-44c9-8379-25db92ab7f3f
    ```
3. Build
   ```sh
   docker compose build
   ```
4. Run
   ```sh
   docker compose up
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] A
- [x] B
- [ ] C
- [ ] D

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[FastAPI-url]: https://fastapi.tiangolo.com/
[FastAPI-logo]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[Postgresql-url]: https://www.postgresql.org/
[Postgresql-logo]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white