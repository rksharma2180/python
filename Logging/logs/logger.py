import logging
logging.basicConfig(
    filename='program.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'#,
    #force=True # Sometime we have to put this to make config work
)