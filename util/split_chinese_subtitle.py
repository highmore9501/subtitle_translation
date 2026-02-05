# 使用正则表达式匹配并移除行首的数字加点号模式
import re


def extract_srt_text(srt_file_path, output_file_path=None):
    """
    从SRT字幕文件中提取文本内容，并用'|'连接成一行

    参数:
    srt_file_path (str): SRT文件的路径
    output_file_path (str, optional): 输出文件路径，如果不提供则不保存到文件

    返回:
    str: 用'|'连接的所有字幕文本
    """

    # 存储提取的文本
    subtitle_texts = []

    try:
        # 读取SRT文件
        with open(srt_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 按空行分割字幕块
        subtitle_blocks = content.strip().split('\n\n')

        for block in subtitle_blocks:
            if block.strip():
                lines = block.split('\n')
                # 字幕文本通常从第3行开始（索引为2）
                # 跳过序号行和时间码行
                if len(lines) >= 3:
                    # 提取文本行（从第3行到最后）
                    text_lines = lines[2:]
                    # 合并多行文本
                    subtitle_text = ' '.join(text_lines).strip()
                    if subtitle_text:
                        subtitle_texts.append(subtitle_text)

        # 用'|'连接所有文本
        result = '|'.join(subtitle_texts)

        # 如果提供了输出文件路径，则保存到文件
        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            print(f"结果已保存到: {output_file_path}")

        return result

    except FileNotFoundError:
        print(f"错误: 找不到文件 {srt_file_path}")
        return None
    except Exception as e:
        print(f"处理文件时出错: {e}")
        return None


def merge_subtitles(chinese_srt_path, english_txt_path, output_srt_path):
    """
    将中文SRT字幕文件与英文翻译文本合并生成双语字幕文件
    在每条中文字幕下方直接添加对应的英文字幕

    Args:
        chinese_srt_path (str): 中文SRT字幕文件路径
        english_txt_path (str): 英文翻译文本文件路径（按行分隔）
        output_srt_path (str): 输出的双语字幕文件路径
    """

    # 读取中文SRT文件
    with open(chinese_srt_path, 'r', encoding='utf-8') as f:
        chinese_lines = f.readlines()

    # 解析SRT文件，提取时间轴和文本内容
    subtitles = []
    i = 0
    while i < len(chinese_lines):
        if chinese_lines[i].strip().isdigit():
            # 获取序号
            number = chinese_lines[i].strip()

            # 获取时间轴
            time_line = chinese_lines[i+1].strip()

            # 获取文本内容（可能跨多行）
            text_lines = []
            j = i + 2
            while j < len(chinese_lines) and chinese_lines[j].strip() != "":
                text_lines.append(chinese_lines[j].strip())
                j += 1

            subtitles.append({
                'number': number,
                'time': time_line,
                'text_lines': text_lines  # 保持原文本行
            })

            i = j + 1 if j < len(chinese_lines) else j
        else:
            i += 1

    # 读取英文翻译文本（按行读取）
    with open(english_txt_path, 'r', encoding='utf-8') as f:
        english_sentences = [line.strip()
                             for line in f.readlines() if line.strip()]

    # 处理英文语句，删除以逗号结尾的逗号
    processed_english_sentences = []
    for sentence in english_sentences:
        if sentence.endswith(','):
            sentence = sentence[:-1].strip()

            # 匹配行首的数字后跟点号和空格的模式
        cleaned_line = re.sub(r'^\d+\.\s*', '', sentence)
        processed_english_sentences.append(cleaned_line)

    english_sentences = processed_english_sentences

    # 检查句子数量是否匹配
    chinese_sentence_count = len(subtitles)
    english_sentence_count = len(english_sentences)

    print(f"中文句子数量: {chinese_sentence_count}")
    print(f"英文句子数量: {english_sentence_count}")

    if chinese_sentence_count != english_sentence_count:
        raise ValueError(
            f"句子数量不匹配！中文: {chinese_sentence_count}, 英文: {english_sentence_count}")

    # 生成双语字幕文件（中英文字幕在同一时间轴下）
    with open(output_srt_path, 'w', encoding='utf-8') as f:
        for i, subtitle in enumerate(subtitles):
            # 写入序号
            f.write(f"{subtitle['number']}\n")
            # 写入时间轴
            f.write(f"{subtitle['time']}\n")
            # 写入中文字幕
            for text_line in subtitle['text_lines']:
                f.write(f"{text_line}\n")
            # 写入英文字幕
            f.write(f"{english_sentences[i]}\n")
            # 空行分隔
            f.write("\n")

    print(f"双语字幕已保存到: {output_srt_path}")


def convert_pipes_to_lines(file_path):
    """
    读取文本文件，将其中的'|'分隔符转换为实际的换行符，并重新写入文件

    参数:
    file_path (str): 需要处理的文本文件路径

    返回:
    bool: 处理成功返回True，失败返回False
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 按'|'分割内容
        lines = content.split('|')
        count = 1

        # 将分割后的内容按行写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                # 去除每行前后的空白字符后写入
                clean_line = line.strip()
                if clean_line:  # 只写入非空行
                    file.write(str(count)+'.'+clean_line + '\n')
                    count += 1

        print(f"文件 {file_path} 处理完成，'|' 已转换为实际换行符")
        return True

    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        return False
    except Exception as e:
        print(f"处理文件时出错: {e}")
        return False


def shift_english_subtitles(srt_file_path, start, end):
    """
    将SRT文件中指定范围的英文字幕在字幕块内向下移动一行（与下一行交换位置）

    参数:
    srt_file_path (str): SRT文件路径
    start (int): 开始字幕块序号（包含）
    end (int): 结束字幕块序号（包含）

    返回:
    bool: 处理成功返回True，失败返回False
    """
    try:
        # 读取SRT文件
        with open(srt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 解析字幕块
        subtitle_blocks = []
        i = 0
        while i < len(lines):
            if i < len(lines) and lines[i].strip().isdigit():
                block_start = i
                # 查找当前字幕块的结束位置
                j = i + 1
                while j < len(lines) and lines[j].strip() != "":
                    j += 1
                # 记录字幕块的起始和结束位置
                subtitle_blocks.append((block_start, j))
                i = j + 1 if j < len(lines) else j
            else:
                i += 1

        # 处理指定范围内的字幕块
        for block_idx in range(len(subtitle_blocks)):
            block_start, block_end = subtitle_blocks[block_idx]
            # 获取当前字幕块的序号
            block_number = int(lines[block_start].strip())

            # 检查是否在处理范围内
            if start <= block_number <= end:
                # 在当前字幕块中找到中英文内容行
                time_line_index = -1
                text_lines_start = -1

                # 查找时间行
                for i in range(block_start + 1, block_end):
                    if '-->' in lines[i]:
                        time_line_index = i
                        text_lines_start = i + 1
                        break

                # 如果找到了时间行
                if time_line_index != -1 and text_lines_start < block_end:
                    # 获取文本行
                    text_lines = []
                    text_line_indices = []

                    for i in range(text_lines_start, block_end):
                        if lines[i].strip() != "":
                            text_lines.append(lines[i])
                            text_line_indices.append(i)

                    # 如果至少有两行文本（中英文）
                    if len(text_lines) >= 2:
                        # 交换倒数第一行和倒数第二行的内容（英文字幕向下移动）
                        last_index = len(text_line_indices) - 1
                        second_last_index = len(text_line_indices) - 2

                        if last_index >= 1:
                            last_line_idx = text_line_indices[last_index]
                            second_last_line_idx = text_line_indices[second_last_index]

                            # 交换两行内容
                            lines[last_line_idx], lines[second_last_line_idx] = \
                                lines[second_last_line_idx], lines[last_line_idx]

        # 将修改后的内容写回文件
        with open(srt_file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        print(f"已处理文件 {srt_file_path}，将第{start}到{end}个字幕块内的英文字幕向下移动一行")
        return True

    except FileNotFoundError:
        print(f"错误: 找不到文件 {srt_file_path}")
        return False
    except Exception as e:
        print(f"处理文件时出错: {e}")
        return False


def srt_to_html(srt_file_path, html_file_path):
    """
    将SRT字幕文件转换为HTML格式

    Args:
        srt_file_path (str): SRT文件路径
        html_file_path (str): 输出HTML文件路径
    """
    with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
        content = srt_file.read()

    # 分割字幕块
    subtitle_blocks = content.strip().split('\n\n')

    print(f"找到 {len(subtitle_blocks)} 个字幕块")

    # 创建HTML内容
    html_content = '''<!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>字幕内容</title>
    </head>
    <body>
    '''

    for block in subtitle_blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:  # 确保有足够的行数
            # 第一行是序号，跳过
            # 第二行是时间戳
            timestamp = lines[1]
            # 第三行及之后是字幕文本
            subtitle_text = '<br>'.join(lines[2:])

            html_content += f'    <p>{subtitle_text}</p>\n'

    html_content += '''</body>
</html>'''

    # 写入HTML文件
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
