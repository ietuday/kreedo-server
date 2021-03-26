import environ
""" Email Configuration"""
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
# environ.Env.read_env()
environ.Env.read_env('.env')


EMAIL_PORT = 587
# EMAIL_PORT = 465
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
