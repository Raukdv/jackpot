from .settings import BASE_DIR, MIDDLEWARE


DEBUG = False


ALLOWED_HOSTS = [
    'api-talentshow.herokuapp.com',
]


MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = BASE_DIR / 'staticfiles'
