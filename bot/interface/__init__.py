def generateErrorNotification(text, id):
    return f'{"ОПОВЕЩЕНИЕ":❌^12}\n' \
           f'Паркинг №{id}:\n' \
           f'{text}'


class Texts:
    start_about = "Добро пожаловать!\n" \
                  "Это бот для управлением стендами a1park."

    main_menu = f"{'Главное меню':🚗^20}\n" \
                f"/find - поиск парковки\n" \
                f"/exit - выйти"

    find_parking = "Введите id паркинга:"
    not_found_parking = "❌Паркинг не найден❌"

    error = "Error: \n❌{}❌"

    class Auth:
        start = "Для продолжения введите token:"
        error = "❌НЕВЕРНЫЙ ТОКЕН❌"

