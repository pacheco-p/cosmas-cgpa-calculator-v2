import bcrypt
import database


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def register(username, email, password):

    hashed = hash_password(password)

    try:
        database.cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, hashed)
        )

        database.conn.commit()

        return True

    except:

        return False


def login(username, password):

    database.cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = database.cursor.fetchone()

    if not user:
        return False

    return check_password(password, user[0])