class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string.")

    def save(self, conn):
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
            )
        conn.commit()

    def articles(self, conn):
        cursor = conn.execute("SELECT id, title, magazine_id FROM articles WHERE author_id=?", (self._id,))
        return cursor.fetchall()
    
    def magazines(self, conn):
        cursor = cursor.execute("""
        SELECT DISTINCT m.* FROM magazines mJOIN articles a ON m.id = a.magazine_idWHERE a.author_id = ?""", (self.id,))
        return cursor.fetchall()
 
    @classmethod
    def top_author(cls, conn):
       cursor = cursor.execute("""
       SELECT au.*, COUNT(a.id) AS article_countFROM authors auJOIN articles a ON au.id = a.author_idGROUP BY au.idORDER BY article_count DESCLIMIT 1""")
       return cursor.fetchone()
