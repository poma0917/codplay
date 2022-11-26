words = ["씨발련아, 개버러지년아, 장애인년아, 느금마, 개씹새끼, 좆까씨발아, ㅗㅗ이거나먹어라, 개새끼, 병신, 개씨발패륜아새끼"]

chat = 0

new_york = 0

bad_word = 0

while True:
    if chat == "관리자 모드":
        new_york = input()
        words.append(new_york)
        print(f"{new_york}추가")
        print(words)
        continue
        words =+ new_york
    chat = input("ㅈㅈㅅ>>")
    bad_word = 0
    new_york = 0
    for i in words:
        if i in chat:
            bad_word += 1
    if bad_word > 0:
        print(f"배드 단어{bad_word}개")
    else:
        print(chat)


            




