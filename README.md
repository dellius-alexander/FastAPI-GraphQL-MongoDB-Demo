[![Testing FastAPI, GraphQL, MongoDB, using Docker Compose](https://github.com/dellius-alexander/FastAPI-GraphQL-MongoDB-Demo/actions/workflows/api-tests.yml/badge.svg)](https://github.com/dellius-alexander/FastAPI-GraphQL-MongoDB-Demo/actions/workflows/api-tests.yml)

# Demo FastAPI, GraphQL and MongoDB Integration

This project integrates FastAPI, GraphQL and MongoDB to create a powerful and flexible API. 
FastAPI provides a fast and secure platform for building RESTful APIs. GraphQL enables 
efficient data fetching, allowing clients to request only the data they need. MongoDB is 
used as a database to store and retrieve data quickly and reliably. Together, these 
technologies provide an efficient and secure way to build a web application/API with dynamic data.

## Getting Started

- `This project serves as a great template for building a FastAPI, GraphQL and MongoDB API from scratch.`

### Prerequisites

The following software is required to be installed on your system to support GraphQL API development, 
MongoDB database management, FastAPI development, and Docker containerization:

- [Python 3.7+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/) 
- [Docker Compose Documentation](https://docs.docker.com/compose/) (optional)
- [MongoDB Express Documentation](https://github.com/mongo-express/mongo-express) (optional)
- [Postman](https://www.postman.com/downloads/) (optional)


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dellius-alexander/FastAPI-GraphQL-MongoDB-Demo.git
   ```
2. Install Python packages
   ```sh
    pip install -r requirements.txt
    ```
3. Start the FastAPI server, MongoDB database and Mongo Express Server
   - Start all services using docker-compose.yml file
      
     ```sh
      docker-compose up -d --build --force-recreate --remove-orphans --renew-anon-volumes
     ```
     
   - Start the FastAPI server locally and use docker-compose.yml file to start the MongoDB database and Mongo Express Server
      
     ```sh
      # comment out the app service in docker-compose.yml file and run the below command
      # after restarting docker-compose, you can access the FastAPI server locally at http://localhost:8000
       python3 -m uvicorn  src.main:app --proxy-headers  --host "0.0.0.0" --port 8000 --reload
     ```
     
4. Test the GraphQL API using the GraphiQL interface at http://localhost:8000/user
   - *Note: You can specify any name for the GraphQL API endpoint*

   ```sh
   # Test data is loaded at initialization of application
    curl -X POST http://localhost:8000/user \
   -H "Content-Type: application/json" \
   -d '{"query": "{ search(email: \"brian@example.com\") { name, email, age, roles, password, lastUpdated } }"}'

   ```
   
5. Start coding your own GraphQL API in the `src` directory. Add your code and modifications to the `src` directory. 
Remember the entrypoint is `src/main.py` or `src.main:app`.

