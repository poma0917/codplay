import random
nums = []
num = 0
while len(nums) < 10:
    num = random.randint(0, 100)
    if num in nums:
        continue
    else:
        nums.append(num)
print(nums)
c = 0
while True:
    q1 = 0
    for n in range(len(nums) - 1):
        if nums[n] > nums[n + 1]:
            nums[n], nums[n + 1] = nums[n + 1], nums[n]
            q1 += 1
            c += 1
    if q1 == 0:
        break

print(nums)
print(f"{c}번 만에 정렬 완료")