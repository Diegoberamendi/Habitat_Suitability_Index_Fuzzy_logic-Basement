from config import logging


def logger(fun):
    def wrapper(*args, **kwargs):
        starting_log()
        fun(*args, **kwargs)
        logging.shutdown()

    return wrapper


def starting_log():
    logging.basicConfig(filename='my-logfile.log',
                        format='%(asctime)s - %(name)s - %(message)s',
                        filemode='w', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug('This message is logged to the file.')
    logging.info('Less severe information is also logged to the file.')



