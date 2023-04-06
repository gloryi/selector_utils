import random

def tournir_sort(data):
    partially_sorted = []
    binary_tier = data[::]
    next_tier = []
    reminders = []
    comparisons = 0
    is_sorted = False
    while not is_sorted:
        if len(binary_tier) > 0:
            a = binary_tier.pop(random.randint(0, len(binary_tier)-1))
            b = binary_tier.pop(random.randint(0, len(binary_tier)-1))

            comparisons += 1
            if a >= b:
                print(f"{a} > {b}")
                next_tier.append(a)
                reminders.append(b)
            else:
                print(f"{b} > {a}")
                next_tier.append(b)
                reminders.append(a)
        else:
            if len(next_tier) > 1:
                print(reminders)
                print(next_tier)
                print()
                partially_sorted += reminders
                binary_tier = next_tier[::]
                reminders = []
                next_tier = []
            else:
                partially_sorted += reminders
                partially_sorted += next_tier
                is_sorted = True
    return partially_sorted, comparisons

#  def partial_sort_pairs(data):
    #  partially_sorted = []
    #  binary_tier = data[::]
    #  next_tier = []
    #  reminders = []
    #  comparisons = 0
    #  is_sorted = False
#
    #  while not is_sorted:
        #  if len(binary_tier) >= 3:
            #  a = binary_tier.pop(random.randint(0, len(binary_tier)-1))
            #  b = binary_tier.pop(random.randint(0, len(binary_tier)-1))
            #  c = binary_tier.pop(random.randint(0, len(binary_tier)-1))
            #  score = 0
            #  comparisons += 1
            #  if a >= b:
                #  score += 1
            #  comparisons += 1
            #  if a >= c:
                #  score += 1
            #  if score == 2:
                #  print(f"{a} > {b} || {c}")
                #  next_tier.append(a)
                #  binary_tier.append(b)
                #  binary_tier.append(c)
            #  if score == 1:
                #  binary_tier.append(a)
                #  binary_tier.append(b)
                #  binary_tier.append(c)
            #  if score == 0:
                #  print(f"{a} < {b} || {c}")
                #  reminders.append(a)
                #  binary_tier.append(b)
                #  binary_tier.append(c)
        #  elif len(binary_tier) == 3:
            #  a, b, c = binary_tier
            #  binary_tier = []
            #  comparisons += 2
            #  if a>= b and a>= c:
                #  next_tier.append(a)
                #  reminders.append(b)
                #  reminders.append(c)
            #  elif b>= a and b>= c:
                #  comparisons += 2
                #  next_tier.append(b)
                #  reminders.append(a)
                #  reminders.append(c)
            #  else:
                #  comparisons += 2
                #  next_tier.append(c)
                #  reminders.append(a)
                #  reminders.append(b)
        #  elif len(binary_tier) == 2:
            #  a, b = binary_tier
            #  binary_tier = []
            #  comparisons += 1
            #  if a>=b :
                #  next_tier.append(a)
                #  reminders.append(b)
            #  else:
                #  next_tier.append(b)
                #  reminders.append(a)
        #  else:
            #  reminders.append(binary_tier[0])
            #  binary_tier = []
#
        #  if len(binary_tier) == 0:
            #  if len(next_tier) > 1:
                #  print(reminders)
                #  print(next_tier)
                #  print()
                #  partially_sorted += reminders
                #  binary_tier = next_tier[::]
                #  reminders = []
                #  next_tier = []
            #  else:
                #  partially_sorted += reminders
                #  partially_sorted += next_tier
                #  is_sorted = True
    #  return partially_sorted, comparisons
#




random_array = list(random.randint(0,10**random.randint(1,5)) for _ in range(512))

print(random_array)

#  part_sorted, comparisons = partial_sort_pairs(random_array)
part_sorted2, comparisons2 = tournir_sort(random_array)
#  full_sorted = sorted(random_array)

#  for n1, n2, n3 in zip(part_sorted, part_sorted2, full_sorted):
    #  print(n1, n2, n3)
print(comparisons2)
