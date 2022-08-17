import os


def export_vars(request):
    return {
        'COMPANY_ADDRESS': '',
        'COMPANY_NAME': 'Furry System',
        'DEBUG': bool(os.environ.get('DEBUG', False)),
        'DJANGO_COLORS': 'light',
    }
