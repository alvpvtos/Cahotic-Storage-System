# The image created by this Dockerfile will not work unless there is a database with the following configuration
    #   and default port (5432) running on the host machine or network.

            # When running with docker compose
            # DATABASE_URL = "postgresql+psych2://username:password@db/dname"
            # When running without docker compose
            # DATABASE_URL = "postgresql+psych2://username:password@localhost/dname"



FROM python:3.11


#copy and install dependencies 
COPY ./requirements.txt  /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#copy source code files
COPY db   /code/db
COPY api   /code/api

#Setup database


# Run fastapi application  (ran every time container is ran? )
CMD ["sh", "-c", " python code/db/dbconfig.py &&  fastapi run code/api/main.py --port 8080"]

#   Install python base image
#   Install python dependencies fastapi==0.115.6 fastapi[standard]==0.115.6 pydantic==2.10.0 psycopg2-binary==2.9.10 sqlalchemy==2.0.36
#   Copy api and db directories into container
#   Run command to configure database
#   Run command to start the API server
#   
