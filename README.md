#How to run:
1. clone repo
2. create env file: .env: $ cp .env-template .env
3. in main folder: $ docker compose build
4. after image is build: $ docker compose up (note: steps below are for alembic)
5. create virtual environment in a new terminal tab: $ python3 -m venv venv
6. activate virtual environment: $ . venv/bin/activate
7. install packages: $ pip3 install -r requirements-dev.txt
8. make alembic migrations: $ alembic upgrade head


API should be available at: http://localhost:5500/docs
