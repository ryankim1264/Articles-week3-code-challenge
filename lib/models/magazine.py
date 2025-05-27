import sqlite3

class Magazine:
    def __init__(self, name, category):
        self._id = None  
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 0 < len(value) <= 255:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string up to 255 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and 0 < len(value) <= 255:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string up to 255 characters.")

    def save(self, conn):
        """Save the magazine to the database (insert or update)."""
        cursor = conn.cursor()

        if self._id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self._id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self._id)
            )

        conn.commit()
        
        
    def articles(self, conn):
        cursor = conn.execute("SELECT id, title, author_id FROM articles WHERE magazine_id=?", (self._id,))
        return cursor.fetchall()

    def contributors(self, conn):
        cursor = conn.execute("""
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._id,))
        return cursor.fetchall()
    
    def magazines_with_multiple_authors(cls, conn):
        cursor = cursor.execute("""
        SELECT m.*, COUNT(DISTINCT a.author_id) AS author_count
        FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        HAVING author_count >= 2
    """)
        return cursor.fetchall()
    

    def articles_count_per_magazine(cls, conn):
        cursor = cursor.execute("""
        SELECT m.id, m.name, COUNT(a.id) AS article_count
        FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
    """)
        return cursor.fetchall()
    
    def contributing_authors(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT au.*, COUNT(a.id) AS article_count
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING article_count > 2
        """, (self.id,))
        return cursor.fetchall()

    