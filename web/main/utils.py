from django.utils.text import slugify as _slugify


def slugify(value):
    slug = _slugify(value, allow_unicode=True)
    slug = slug.replace('ş', 's')
    slug = slug.replace('ç', 'c')
    slug = slug.replace('ö', 'o')
    slug = slug.replace('ı', 'i')
    slug = slug.replace('ü', 'u')
    slug = slug.replace('ğ', 'g')
    return slug
