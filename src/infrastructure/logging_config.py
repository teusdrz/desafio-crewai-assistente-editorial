# Logging Configuration for Editorial Assistant
# Provides comprehensive logging for debugging and monitoring

import logging
import logging.config
import os
from datetime import datetime
from functools import wraps

def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
    """
    Setup comprehensive logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to file in addition to console
    """
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if log_to_file and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Logging configuration
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(name)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console'],
                'level': log_level,
                'propagate': False
            },
            'src.application.use_cases': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': False
            }
        }
    }
    
    # Add file handler if requested
    if log_to_file:
        timestamp = datetime.now().strftime("%Y%m%d")
        config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': log_level,
            'formatter': 'detailed',
            'filename': f'{log_dir}/editorial_assistant_{timestamp}.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        }
        
        # Add file handler to loggers
        config['loggers']['']['handlers'].append('file')
        config['loggers']['src.application.use_cases']['handlers'].append('file')
    
    logging.config.dictConfig(config)

def get_logger(name: str) -> logging.Logger:
    """Get logger instance with proper configuration"""
    return logging.getLogger(name)

# Performance monitoring decorator
def log_performance(func):
    """Decorator to log function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(f"{func.__module__}.{func.__name__}")
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Function {func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Function {func.__name__} failed after {duration:.3f}s: {str(e)}")
            raise
    
    return wrapper
