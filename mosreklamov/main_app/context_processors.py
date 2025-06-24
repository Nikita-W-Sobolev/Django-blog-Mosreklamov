from main_app.views import main_menu, tags, categories_list


# Это контекстный процессор. Импортируем любые переменные и они появятся везде!
# Нужно лишь только зарегистрировать в settings.py в коллекции TEMPLATES -> 'context_processors' -> 'users.context_proc.get_women_context'
# Всё, что пропишем в возвращаемом словаре будет доступно во всех шаблонах. Очень удобно!
def global_context(request):
    return {
        'data': main_menu,
        'tags': tags,
        'categories': categories_list,
    }