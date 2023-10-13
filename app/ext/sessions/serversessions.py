from flask import session


def get_current_session():
    """
    using default flask session
    """
    return session


def terminate_session():
    session.clear()
