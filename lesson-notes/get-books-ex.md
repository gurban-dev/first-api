## Write a function that retrieves all books from the database.

1. **Establish a database connection** using `get_connection()`.

2. **Execute an SQL query** to retrieve every row from the `books` table.
   ```python
   cursor = connection.execute("SELECT * FROM books")
   ```

3. **Retrieve all results** from the `sqlite3.Cursor` object using `.fetchall()`.
   
   - `connection.execute()` returns a `sqlite3.Cursor` object.
   - Use `cursor.fetchall()` to retrieve all rows.

4. **Close the database connection** once the data has been retrieved.

5. **Convert the retrieved rows into a list of Python dictionaries.**
   ```python
   books_list = []

   for book in books:
       books_list.append(dict(book))
   ```

6. **Return the resulting list** of dictionaries.