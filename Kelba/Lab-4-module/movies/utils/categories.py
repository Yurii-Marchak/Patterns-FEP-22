from movies.models import Category

def get_all_categories():
    """
    Отримує всі категорії з бази даних.
    :return: QuerySet з усіма категоріями.
    """
    categories = Category.objects.all()
    return categories