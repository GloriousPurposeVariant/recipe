LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  
            'class': 'logging.FileHandler',
            'filename': 'logs/django_execution.log', 
            'formatter': 'verbose',
        },
        # 'error_file': {
        #     'level': 'WARNING',  
        #     'class': 'logging.FileHandler',
        #     'filename': 'logs/django_errors.log',  
        #     'formatter': 'verbose',
        # },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',  
            'propagate': True,
        },
        'users': { 
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'recipe': { 
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
