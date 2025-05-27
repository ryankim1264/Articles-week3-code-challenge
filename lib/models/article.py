import sqlite3

class Article:
    def __init__(self, title, author_id, magazine_id):
        self._id = None
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 0 < len(value) <= 255:
            self._title = value
        else:
            raise ValueError("Title must be a non-empty string up to 255 characters.")

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if isinstance(value, int) and value > 0:
            self._author_id = value
        else:
            raise ValueError("Author ID must be a positive integer.")

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if isinstance(value, int) and value > 0:
            self._magazine_id = value
        else:
            raise ValueError("Magazine ID must be a positive integer.")

    def save(self, conn):
        """Insert or update the article in the database."""
        cursor = conn.cursor()

        if self._id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self._id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self._id)
            )

        conn.commit()