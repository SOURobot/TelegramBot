def ans(command):
    if command == "/start":
        return "Привет!\nМеня зовут Cheap & Daily и я телеграм-бот.\nХотите выбраться из Москвы и куда-нибудь слетать? Тогда вам ко мне! Я помогу найти самые выгодные билеты, удовлетворяющие вашим пожеланиям.\nНу что, начнем?\nТогда нажимайте /search и поехали!\nP.S. Не знаете, как со мной работать? Нажмите /help для получения списка команд и прочих инструкций."
    elif command == "/help":
        return "К сожалению, пока я не могу вам ни чем помочь."
    elif command == "/search":
        return "Пиши, короче"
    else:
        return "Я вас не понимаю. Нажмите /help для получения списка команд и прочих инструкций."