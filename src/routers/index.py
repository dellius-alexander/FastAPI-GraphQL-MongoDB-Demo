from starlette.responses import HTMLResponse
# Get the logger
from myLogger.Logger import getLogger as GetLogger
from fastapi import APIRouter
log = GetLogger(__name__)

router = APIRouter()

# -----------------------------------------------------------------------------
html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>GraphQL API Test Page</title>
    <meta charset="utf-8" />
    <script src="https://code.jquery.com/jquery-3.6.4.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <!-- Optional theme -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
    <!-- Latest compiled and minified JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <style>
      body {
        background-color: white;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
      }
       .main {
        margin: 0 auto;
        left: 0;
        right: 0;
        max-width: 100%;
        }
      .container {
        margin: 0 auto;
        left: 0;
        right: 0;
        max-width: 80%;
        padding: 20px;
        background-color: skyblue;
        border-radius: 15px;
      }
        textarea {
        margin: 20px auto;
        left: 0;
        right: 0;
        padding: 15px;
        background-color: white;
        width: 100%;
        max-width: 100%;
        border-radius: 15px;
        }
    </style>
  </head>
  <body>
    <main class="main">
      <div class="container">
        <h1 style="text-align:center;">GraphQL API Test Page</h1>
        <br />
        <div class="query">
          <h2 style="text-align:center;">User Query</h2>
          <label for="query">Query User Data:</label>
          <br />
          <textarea 
            name="query" 
            id="query" 
            placeholder="{users{name,email,age, lastUpdated}}" 
            cols="100" rows="5" 
            wrap="soft" autofocus required /></textarea>
          <br />
          <div class="query-error"></div>
          <button onclick="query(event)">Submit Query</button>
          <br />
          <br />
          <hr />
        </div>
        <div class="mutation">
          <h2 style="text-align:center;">User Mutations</h2>
          <label for="mutation">Create New User:</label>
          <br />
          <textarea 
            name="mutation" 
            id="mutation" 
            placeholder='{createUser(name: "Jackie Brown", email: "jackie@example.com", age: 21, roles: ["subscriber","user"]) { name, email, age }}' 
            cols="100" rows="5"  
            wrap="soft" autofocus required /></textarea>
          <br />
          <div class="mutation-error"></div>
          <button onclick="mutation(event)">Create User</button>
          <br />
          <br />
          <hr />
        </div>
        <h2>Response</h2>
        <div id="response"></div>
      </div>
    </main>
    <script>
        const endpoints = {
        query: "/user",
        mutation: "/user"
        };
        const query_error = document.querySelector(".query-error");
        const mutation_error = document.querySelector(".mutation-error");
        /**
         * Query function that sends query object to the server
         * @description Query
         * @returns {Promise<void>}
         */
        async function query(event) {
            event.preventDefault();
            const query = document.getElementById("query").value;
            //const error = document.querySelector(".query-error");
            try {
                if (!query) {
                    query_error.style.color = "red";
                    query_error.innerHTML = "Please enter a query!";
                    return;
                }
                query_error.innerHTML = "";
                const response = await axios.post(endpoints.query, {
                  query
                });
                const data = document.createElement("pre");
                data.innerHTML = JSON.stringify(response.data, null, 2);
                data.appendChild(document.createElement("hr"));
                document.getElementById("response").appendChild(data);
            } catch (error) {
                console.dir(error.response.data);
                const error_element = document.createElement("pre");
                error_element.style.color = "red";
                error_element.innerHTML = JSON.stringify(error.response.data.errors, null, 2);
                query_error.appendChild(error_element);
            }
        }
        /**
         * Mutation function that sends create, update and delete object to the server
         * @description Mutation
         * @returns {Promise<void>}
         */
        async function mutation(event) {
            const query = document.getElementById("mutation").value;
            //const error = document.querySelector(".mutation-error");
            try {
                if (!query) {
                    mutation_error.style.color = "red";
                    mutation_error.innerHTML = "Please enter new user data!";
                    return;
                }
                mutation_error.innerHTML = "";
                const response = await axios.post(endpoints.mutation, {
                  query
                });
                const data = document.createElement("pre");
                data.innerHTML = JSON.stringify(response.data, null, 2);
                data.appendChild(document.createElement("hr"));
                document.getElementById("response").appendChild(data);
            } catch (error) {
                console.dir(error.response.data);
                const error_element = document.createElement("pre");
                error_element.style.color = "red";
                error_element.innerHTML = JSON.stringify(error.response.data.errors, null, 2);
                mutation_error.appendChild(error_element);
            }
        }
    </script>
  </body>
</html>
"""


# -----------------------------------------------------------------------------
@router.get(
    path="/",
    response_class=HTMLResponse,
    summary="Root endpoint",
    description="Root endpoint",
    tags=["index"],
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad request"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)
async def root() -> HTMLResponse:
    """
    Resolves the root/index endpoint with html content.
    :return: HTMLResponse
    """
    return HTMLResponse(html)


