if __name__ == "__main__":
    from src.rmq import get_connection
    with get_connection() as rmq_connection:
        with rmq_connection.channel() as channel:
            while 1:
                pass
