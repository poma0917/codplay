# -*- coding: utf-8 -*-

drinks = {"솔의 눈": 1000, "맥콜" : 1200, "원비디" : 1000, "비락식혜" : 1200, "칠성사이다" : 1500}


def showcase():
    print("#" * 5, "판매중인 음료수들", "#" * 5)
    print(drinks)
    print("-" * 29)
    print(f"잔액은 {money}원 입니다")
    print("-" * 29)

pick = 0
money = 0

while True:
    showcase()
    input("주문하시겠어요?")
    while True:
        if money >= 1000:
            pass
        else:
            money = input("돈을 넣어주세요 (안사려면 q키를 입력하세요)")
        if money == "q":
            break
        showcase()
        print(f"잔액은 {money}원 입니다")
        pick = input("음료를 골라주세요 (음료 이름을 적어주세요) (그만사려면 q) : ")
        if pick == "q":
            break
        elif int(money) >= drinks[pick]:
            print(f"주문하신 음료 {pick} 나왔습니다")
            money = int(money) - drinks[pick]
        else:
            print("잔액이 부족합니다")
            continue
    if int(money) > 0:
        print(f"거스름돈은 {money}원 입니다. 안녕히 가세요")
        money = 0
