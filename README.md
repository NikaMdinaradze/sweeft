# Technical Assignment for Sweeft

This is a RESTful API for a Book Giveaway Service, where users can offer books for free and also request books offered by others.

## Getting Started

To simplify your experience, I have deployed the API for you.
**Base URL:** `http://34.207.238.175/`

You can also access the Swagger UI for interactive exploration and testing: [`http://34.207.238.175/docs`](http://34.207.238.175/docs)

You have two options to interact with the API:

1. **Docker Image:**
   - Pull the Docker image:
     ```
     docker pull nika04/sweeft:0.1
     ```
   - Run the Docker container:
     ```
     docker run -p 8000:8000 nika04/sweeft:0.1
     ```

2. **GitHub Repository:**
   - Clone the GitHub repository:
     ```
     git clone https://github.com/NikaMdinaradze/sweeft.git
     ```
   - Change working directory:
     ```
     cd sweeft
     ```
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the API using Uvicorn:
     ```
     uvicorn main:app
     ```

   **Note:** It is recommended to use a virtual environment for better isolation.

## Endpoints

**Note:** If you are using this API from your local machine, replace `http://34.207.238.175/` with `localhost`.

### Books Offered

To view the books offered, send a GET request to [`http://34.207.238.175/books/`](http://34.207.238.175/books/) with query parameters: `query` (searches books by title, description, and author) and `genre`. A successful response will return a 200 status code.

You can also retrieve information about registered users by sending a GET request to [`http://34.207.238.175/users/`](http://34.207.238.175/users/).

### Registration and Authentication

To get started offering and requesting books, first, register by sending a POST request to [`http://34.207.238.175/users/`](http://34.207.238.175/users/). Provide your username, email, password and profile (photo). Your registration must meet specific requirements: the username must be unique, the email should be valid, and the password must contain at least one number and one uppercase letter.

After registration, log in using a POST request to [`http://34.207.238.175/users/login`](http://34.207.238.175/users/login) with your username and password. Upon successful login, you will receive a JWT bearer token, allowing you to access your user information via a GET request to [`http://34.207.238.175/users/me`](http://34.207.238.175/users/me) with the provided token.

### Offering and Requesting Books

Now, you can offer books to others by sending a POST request to [`http://34.207.238.175/books/`](http://34.207.238.175/books/). Provide book details such as title, author, genre, description, location, condition and photo. You can also update a book's condition using a PATCH request to [`http://34.207.238.175/books/`](http://34.207.238.175/books/).

If someone requests your book, you can view the requests for that book by sending a GET request to [`http://34.207.238.175/books/`](http://34.207.238.175/books/) with the book ID as a query parameter. You can then choose which request to approve by sending a PATCH request to [`http://34.207.238.175/request/`](http://34.207.238.175/request/) with `approved_status=true`. After giving away the book, delete it with a DELETE request to [`http://34.207.238.175/books/`](http://34.207.238.175/books/) (provide the book ID), and all related requests will be automatically deleted.

If you want to request a book, send a POST request to [`http://34.207.238.175/request/`](http://34.207.238.175/request/) with the `book_id` as a parameter. Once the book's owner approves your request, you can collect the book.

### Explore with Swagger UI

For more details and interactive testing, please use Swagger UI: [`http://34.207.238.175/docs/`](http://34.207.238.175/docs/)

## Conclusion

Thank you for using my API! I hope this documentation helps you get started with our Book Giveaway Service. If you have any advice or questions, please feel free to [contact me](mailto:mdinaradzenika04@gmail.com).

Is this documentation satisfactory? Please let me know if you have any further suggestions or corrections.




