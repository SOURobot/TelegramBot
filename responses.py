def ans(command):
    if command == "/start":
        return """Привет!
                  Меня зовут Cheap & Daily и я телеграм-бот.
                  Хотите выбраться из Москвы и куда-нибудь слетать? Тогда вам ко мне! Я помогу найти самые выгодные билеты, удовлетворяющие вашим пожеланиям.
                  Ну что, начнем?
                  Тогда нажимайте /search и поехали!
                  P.S. Не знаете, как со мной работать? Нажмите /help для получения списка команд и прочих инструкций."""
    elif command == "/help":
        return "К сожалению, пока я не могу вам ни чем помочь."
    elif command == "/search":
        return "Пиши, короче"
    else:
        return "Я вас не понимаю. Нажмите /help для получения списка команд и прочих инструкций."