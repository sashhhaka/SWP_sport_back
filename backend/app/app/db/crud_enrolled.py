import logging
from typing import List

from .crud_users import __tuple_to_student
from ..models.user import Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def reenroll_student(conn, group_id: int, student_id: int):
    """
    Enrolls given student in a group, removes all previous enrollments
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enroll WHERE student_id = %s', (student_id,))
    cursor.execute('INSERT INTO enroll (student_id, group_id, is_primary) VALUES (%s, %s, TRUE)',
                   (student_id, group_id))
    conn.commit()


def enroll_student_to_secondary_group(conn, group_id: int, student_id: int):
    """
    Enrolls given student to a secondary group
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO enroll (student_id, group_id, is_primary) VALUES (%s, %s, FALSE)',
                   (student_id, group_id))
    conn.commit()


def unenroll_student(conn, group_id: int, student_id: int):
    """
    Unenrolls given student from a secondary group
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enroll WHERE group_id = %s AND student_id = %s AND is_primary = FALSE',
                   (group_id, student_id))
    conn.commit()
