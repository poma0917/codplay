import numbers
import random

def wordMemorize():
    pass
kor = ["차", "자동차", "뱀", "돈", "쥐"]
eng = ["tea", "car", "snake", "money", "rat"]
pick = 0 #몇 범째 단어를 꺼낼지 순서를 담아두는 변수
score = 0 #문제를 낼 때마다 올라가는 숫자
answer = 0

while len(eng) > 0:
    pick = random.randint(0, len(kor) - 1)
    score += 1
    answer = input(f"{kor[pick]} <- 이 뜻을 가지는 영어 단어를 쓰시오 : ")
    if answer == eng[pick]:
        print("정답입니다")
        kor.pop(pick)
        eng.pop(pick)
    else:
        print("틀렸습니다")

print("준비한 단어를 모두 외우셨군요")
if score < 6:
    print("당신은 머리가 나쁘지 않습니다")
elif 5 < score <9:
    print("당신은 머리가 좀 나쁘시군요")
else:
    print("당신은 머리가 없으시군요")

def lotto():
    pass
numbers = []
dangchum = []
pick = 0
for i in range(1,46):
    numbers.append(i)

print("로또 번호 추첨해 드림니다")

# for pick in range(7):
#     pick = numbers.pop(random.randint(0, len(numbers) -1))
#     dangchum.append(pick)

dangchum = random.sample(numbers, 7)

print(dangchum)

    
    