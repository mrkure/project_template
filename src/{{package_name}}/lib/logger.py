"""Logger."""

import sys
import time
import logging
from functools import wraps
import pandas

class ColoredLogger(logging.Formatter):
    RESET = "\033[0m"
    WHITE = "\033[37m"  # White
    BLUE = "\033[34m"  # Blue
    YELLOW = "\033[33m"  # Yellow (used for warning)
    RED = "\033[31m"  # Red
    MAGENTA = "\033[35m"  # Magenta (used for critical)
    GREEN = "\033[32m"
    CYAN = "\033[36m"

    def format(self, record):
        """overriden logging.Formatter.format function
        additional format (colors) added after super formatting
        """
        # Define the color for the entire message based on the log level
        if record.levelno == logging.DEBUG:
            color = self.WHITE
        elif record.levelno == logging.INFO:
            color = self.BLUE
        elif record.levelno == logging.WARNING:
            color = self.YELLOW
        elif record.levelno == logging.ERROR:
            color = self.RED
        elif record.levelno == logging.CRITICAL:
            color = self.RED
        else:
            color = self.WHITE
        # Apply color to the entire log message
        formatted_message = f"{color}{super().format(record)}{self.RESET}"
        return formatted_message

    @classmethod
    def setup_logger(cls, module) -> logging.Logger:
        """set logger settings for collored formatting

        Returns:
            logging.Logger: configured logger
        """
        logging.setLoggerClass(logging.Logger)
        _logger = logging.getLogger(module)
        # Clear existing handlers
        for handler in _logger.handlers[:]:  # Create a copy to avoid modifying during iteration
            _logger.removeHandler(handler)
        # Create a new stream handler for stdout
        custom_handler = logging.StreamHandler(sys.stdout)
        custom_handler.setLevel(logging.DEBUG)  # Set level for the custom handler
        # Use the ColoredLogger
        formatter = ColoredLogger("%(asctime)s|%(name)-12s|%(funcName)-22s| %(message)s")
        custom_handler.setFormatter(formatter)
        # Add the custom handler to the logger
        _logger.addHandler(custom_handler)
        # Disable propagation to avoid double logging
        _logger.propagate = False
        # set logging level
        _logger.setLevel(logging.DEBUG)  # Set the logger level
        return _logger


def loggerw(logger):
    """logs function name, params, execution time, results
        list and spark dataframe have special handling
        (checks are done using type(), as isinstance does not work in databricks connect for whatever reason)
    Args:
        logger (logging.logger): logger instance
    """

    def info_arguments(args, kwargs, func):
        def args_to_str(args):
            """replace args"""
            new_args = []
            for arg in args:
                arg = str(arg)
                arg = arg[:30] + " ... " + arg[-30:] if len(arg) > 60 else arg
                new_args.append(arg)
            return " | ".join(new_args)

        def kwargs_to_str(kwargs):
            """replace args"""
            new_kwargs = []
            for k, v in kwargs.items():
                v = str(v)
                v = v[:50] + "..." + v[-50:] if len(v) > 100 else v
                new_kwargs.append(f"{k} = {v}")
            return " | ".join(new_kwargs)

        return " | ".join([i for i in [args_to_str(args), kwargs_to_str(kwargs)] if i])

    def info_return_value(result: tuple):
        if not isinstance(result, tuple):
            _result = (result,)
        else:
            _result = result
        new_results = []
        for arg in _result:
            if isinstance(arg, pandas.DataFrame):
                arg = f"\n{type(arg)}\n{arg.to_string(max_colwidth=100, show_dimensions=True, max_rows=5, justify='center')}\n"
            else:
                arg = str(arg)
                arg = arg[:30] + " ... " + arg[-30:] if len(arg) > 60 else arg
            new_results.append(arg)
        new_result = " | ".join(new_results)
        return new_result

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(">>> def %s <<< ( %s )", func.__name__.lower(), info_arguments(args, kwargs, func))
            start_time = time.time()
            result = func(*args, **kwargs)  # function call
            execution_time = f"Duration: {time.time() - start_time:.0f} (s)"
            logger.debug(">>> def %s <<< return ( %s ) %s\n\n", func.__name__.lower(), info_return_value(result), execution_time)
            return result

        return wrapper

    return decorator
