import parser

page_count = int(input("Введите количество страниц: "))
print('\n')
for page_num in range(1, page_count+1):
    parser.parse(page_num)

