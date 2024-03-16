def split_file(input_file, output_folder, line_count):
    # 打开输入文件并读取内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # 计算文件行数
    total_lines = len(content)

    # 检查指定的行数是否超过文件的总行数
    if line_count > total_lines:
        print("指定的行数超过了文件的总行数")
        return

    # 计算每个小文件的行数
    per_file_lines = total_lines // line_count

    # 循环创建小文件并写入内容
    for i in range(line_count):
        start_index = i * per_file_lines
        end_index = start_index + per_file_lines

        output_file = f"{output_folder}/{i}.txt"
        with open(output_file, 'w', encoding='utf-8') as new_file:
            new_file.writelines(content[start_index:end_index])


# 指定输入文件路径
input_file = r'D:\daily-tasks\github\myfavorite\toutiao\myfavorites-20231118-164500.txt'

# 指定输出文件夹路径
output_folder = r'D:\daily-tasks\github\myfavorite\toutiao\split_files'

# 指定每个小文件的行数
line_count = 100

split_file(input_file, output_folder, line_count)