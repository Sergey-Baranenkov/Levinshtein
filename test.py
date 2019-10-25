def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
  return [[ 0 for col in range(num_cols)] for row in range(num_rows)] #генератор матрицы

def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
  for j in range(1,len(edit_matrix[0])): #заполнение первой строки
      edit_matrix[0][j] = edit_matrix[0][j - 1] + add_weight

  for i in range(1,len(edit_matrix)): # заполнение первого столбца
      edit_matrix[i][0] = edit_matrix[i - 1][0] + remove_weight

  return edit_matrix

def minimum_value(numbers: tuple) -> int: #возвращает минимальное значение из кортежа
    return min(numbers);

def fill_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int, substitute_weight: int) -> list:
    for i in range(1,len(edit_matrix)): #для каждой строки
        for j in range (1,len(edit_matrix[0])): #для каждого элемента строки
            edit_matrix[i][j] = minimum_value((edit_matrix[i-1][j] + remove_weight, #находим минимум
                                               edit_matrix[i][j-1] + add_weight
                                               ,edit_matrix[i-1][j-1] + (substitute_weight if original_word[i-1]!=target_word[j-1]
                                                                                            else 0)))
    return edit_matrix

def find_distance(original_word: str, target_word: str, add_weight: int, remove_weight: int, substitute_weight: int) -> int:
    original_word_len = len(original_word) #длина оригинального слова
    target_word_len   = len(target_word) #длина слова на которое нужно заменить
    #инициализируем матрицу решений
    initialized_matrix = initialize_edit_matrix(generate_edit_matrix(original_word_len+1,target_word_len+1),add_weight,remove_weight)
    #заполняем матрицу решений
    return fill_edit_matrix(initialized_matrix,add_weight,remove_weight,substitute_weight)[original_word_len][target_word_len]
    #возвратили последний элемент главной диагонали - дистанцию

def save_to_csv(edit_matrix: tuple,path_to_file: str) -> None:
  with open(path_to_file, 'w') as file:
      for row in edit_matrix:
          file.write("%s\n" %','.join(str(el) for el in row))#превращаем каждую линию матрицы в строку, разд. запятой

def load_from_csv(path_to_file: str) -> list:
    with open(path_to_file, 'r') as file:
        matrix = []
        for row in file.read().splitlines():
            matrix.append([int(el) for el in row.split(",")]) #превращаем матрицу в матрицу интов
    return matrix

def describe_edits(edit_matrix: tuple,original_word: str,target_word: str,add_weight: int,remove_weight: int,substitute_weight: int) -> list:
    i = len(edit_matrix)-1 #длина ориг слова
    j = len(edit_matrix[0])-1  #длина таргет слова

    #блок проверки непустоты входных слов
    if i==0:
        return ["insert %s"%ch for ch in target_word]
    elif j == 0:
        return ["remove %s" %ch for ch in original_word]
    describeList = [] #создаем список описаний операций

    while i>0 or j>0: #идем по матрице от нижнего правого угла в верхний левый угол
        checkRemoved = edit_matrix[i-1][j] + remove_weight
        checkAdded = edit_matrix[i][j-1] + add_weight
        checkSubstituted = edit_matrix[i-1][j-1] + (substitute_weight if original_word[i-1]!=target_word[j-1] else 0)

        #находим минимум
        minVal = minimum_value((checkRemoved, checkAdded, checkSubstituted))
        #определяем, что делали на каждом шаге (с конца)
        if minVal == checkRemoved:
            describeList.append("remove %s" %original_word[i-1])
            i-=1
            continue
        elif minVal == checkAdded:
            describeList.append("insert %s" %target_word[j-1])
            j-=1
            continue
        elif minVal != edit_matrix[i-1][j-1]:
            describeList.append("substitute %s with %s" %(original_word[i-1],target_word[j-1]))
        j-=1
        i-=1
    return describeList[::-1] #разворачиваем список(т.к изначально действия записаны с конца)

original_word = "length" #начальное слово
target_word = "kitchen" #слово, к которому нужно привести
path_to_file = "table.csv" #путь до файла
#веса
insert_w = 1
remove_w = 1
sub_w = 2

filled_matrix = fill_edit_matrix(initialize_edit_matrix(generate_edit_matrix(len(original_word)+1,len(target_word)+1),
                                                        insert_w,remove_w),
                                 insert_w,remove_w,sub_w)

print("Matrix:")
for row in load_from_csv(path_to_file):
    print(row)
print("Lowest distance:")
print (find_distance(original_word,target_word,insert_w,remove_w,sub_w))
print("Steps:")
print(describe_edits(filled_matrix,original_word,target_word,insert_w,remove_w,sub_w)) #печатаем список изменений
save_to_csv(filled_matrix,path_to_file) #сохраняем
print("From file:")
for row in load_from_csv(path_to_file): #восстанавливаем
    print (row)