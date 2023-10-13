try:
    def terminate_session():
        session = get_current_session()
        if session.is_active():
            session.terminate()

    from gaesessions import SessionMiddleware, get_current_session
except ImportError:
    from serversessions import get_current_session, terminate_session
