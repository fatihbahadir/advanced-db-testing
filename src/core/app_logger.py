import logging

class Logger:
    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initialize the Logger class.
        
        Parameters:
            name (str): The name of the logger.
            level (int): The logging level.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(ch)

    def get_logger(self):
        """
        Get the logger instance.
        
        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger