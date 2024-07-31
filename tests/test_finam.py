'''https://www.online-python.com/
Python

1)Функция для преобразования строки, которая заменяет каждый уникальный символ в входной строке на "(",
и каждый символ, который встречается более одного раза, на ")".

Текст ввода: "the-stealth-warrior".
Текст вывода: "))))()))()))()))(()".'''

text = "the-stealth-warrior"
new_new_str = ''

for i in text:
    if len([item for item in text if item == i]) == 1:
        new_new_str += '('
    elif len([item for item in text if item == i]) > 1:
        new_new_str += ')'

print(new_new_str)


