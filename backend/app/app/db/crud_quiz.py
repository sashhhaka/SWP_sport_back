from typing import List, Tuple


def create_quiz(conn, author_id: int):
    """
    Creates new quiz, quiz is marked as active by default
    @param conn - Database connection
    @param author_id: int - quiz author id
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO quiz (author_id) VALUES (%s)', (author_id,))
    conn.commit()


def insert_priorities(conn, user_id: int, quiz_id: int, priorities: List[Tuple[int, int]]):
    """
    Records selected priorities for given user
    @param conn - Database connection
    @param user_id: int - id of user, who marked priorities
    @param quiz_id: int - current quiz id
    @param priorities: list - list of tuples (group_id, priority)
    """
    cursor = conn.cursor()
    for (group, priority) in priorities:
        cursor.execute('INSERT INTO selected_priority (user_id, quiz_id, group_id, priority) VALUES (%s, %s, %s, %s)',
                       (user_id, quiz_id, group, priority))
    conn.commit()


def check_if_user_have_submission(conn, quiz_id: int, user_id: int) -> bool:
    """
    Checks if given user already participated in a given quiz
    @param conn - Database connection
    @param quiz_id: int - current quiz id
    @param user_id: int - searched user id
    @return True, if a given user already has submission
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM selected_priority WHERE user_id=%s AND quiz_id=%s LIMIT 1', (user_id, quiz_id))
    return cursor.fetchone() is not None


def delete_submission(conn, quiz_id: int, user_id: int):
    """
    Clears submission for a particular user in given quiz, deletes all priority records from previous submission
    @param conn - Database connection
    @param quiz_id: int - current quiz id
    @param user_id: int - searched user id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM selected_priority WHERE user_id=%s AND quiz_id=%s', (user_id, quiz_id))
    conn.commit()
