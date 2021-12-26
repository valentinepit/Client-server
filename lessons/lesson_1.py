def task_1():
    words = {"разработка": "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",
             "сокет": "\u0441\u043e\u043a\u0435\u0442",
             "декоратор": "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440",
             }
    for item in words:
        print(f"Слово - {item} *** Тип -{type(item)}\n В UTF-8 \n Слово - {words[item]} *** Тип - {type(words[item])}")


def task_2():
    words = ["class", "function", "method"]
    for word in words:
        print(eval("b'word'"))


def task_3():
    flag = False
    words = ["attribute", "класс", "функция", "type"]
    for word in words:
        uni_word = word.encode("utf-8")
        for letter in word:
            if ord(letter) > 127:
                flag = True
                break
        if flag:
            print(f"слово {word} нельзя представить в байтовом виде {uni_word}")
        else:
            print(f"Перекодировка показала {word} в байтовом виде {uni_word}")


def task_4():
    words = ["разработка",
             "администрирование",
             "protocol",
             "standard",
             ]
    for word in words:
        print(f"Слово {word} в байтовом виде: {word.encode('utf-8')}")
        print(f"Обратная перекодировка: {word.encode('utf-8').decode('utf-8')}")


def task_5():
    import subprocess
    import chardet
    import platform
    targets = ["yandex.ru",
               "youtube.com",
               ]
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for target in targets:
        args = ['ping', param, '2', target]
        subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in subproc_ping.stdout:
            result = chardet.detect(line)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


def task_6():
    name = "test.txt"
    encoding = file_encoding_detect(name)
    with open(name, encoding=encoding) as f:
        content = f.read()
    print(content)


def file_encoding_detect(_name):
    from chardet import detect
    with open(_name, 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    return encoding


def main():
    while True:
        try:
            task = int(input('Введите номер задачи. Для выхода введите 0: '))
        except ValueError:
            print("Номера задач от 1 до 6")
            continue
        if task == 1:
            task_1()
        elif task == 2:
            print("К сожалению вторая задача не решена")
        elif task == 3:
            task_3()
        elif task == 4:
            task_4()
        elif task == 5:
            task_5()
        elif task == 6:
            task_6()
        elif task == 0:
            break
        else:
            print("Номера задач от 1 до 6")


if __name__ == "__main__":
    main()

