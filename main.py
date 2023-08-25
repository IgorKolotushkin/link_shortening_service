from messages import Message


def main():
    print("Программа для сокращения интернет-адресов\n")
    while True:
        Message.show_menu()
        try:
            result = int(input("Ваш выбор: "))
            if result < 1 or result > 5:
                raise ValueError
            if result in [1, 2, 3, 4]:
                message = Message.get_answer(menu_id=result)
                message.message()
            else:
                break
        except ValueError:
            print("Это должно быть число от 1 до 5")


if __name__ == "__main__":
    main()
