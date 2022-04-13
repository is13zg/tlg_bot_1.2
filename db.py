import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def book_exists(self, name):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `books_view_count` WHERE `name` = ?", (name,)).fetchmany(1)
            return bool(len(res))

    def add_book(self, name, count):
        with self.connection:
            return self.cursor.execute("INSERT INTO `books_view_count` (`name`,`view_count`) VALUES (?,?)",
                                       (name, count))

    def add_book_view(self, name):
        with self.connection:
            return self.cursor.execute("UPDATE `books_view_count` SET `view_count` = `view_count` + 1 WHERE `name`=?",
                                       (name,))

    def get_books_stat(self):
        with self.connection:
            return self.cursor.execute("SELECT `name`, `view_count` FROM `books_view_count`").fetchall()

    def user_exists(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(res))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def count_users(self):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) from `users`").fetchmany(1)

    def count_active_user(self):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) from `users`  WHERE `active` = 1").fetchmany(1)

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id`=?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `active` FROM `users`").fetchall()

    def admin_exists(self, admin_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM `admins` WHERE `admin_id` = ?", (admin_id,)).fetchmany(1)
            return bool(len(res))

    def add_admin(self, admin_id, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `admins` (`admin_id`,name) VALUES (?,?)", (admin_id, name,))

    def del_admin(self, admin_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `admins` WHERE `admin_id` = ?", (admin_id,))

    def get_admins(self):
        with self.connection:
            return self.cursor.execute("SELECT `admin_id`,`name` FROM `admins`").fetchall()
