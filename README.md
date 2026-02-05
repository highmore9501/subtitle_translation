> ⚠️ **AI生成声明**: 本文档由AI助手生成，旨在提供使用指导。如发现任何不准确或遗漏之处，请以实际代码功能为准，通常不会影响工具的正常使用。

# 字幕翻译工具 (Subtitle Translation Tool)

这是一个专门用于处理SRT字幕文件翻译的Python工具包，支持从中文字幕提取、机器翻译到生成双语字幕的完整流程。

## 功能特性

- 🎯 **智能提取**: 自动从SRT字幕文件中提取纯文本内容
- 🔧 **格式转换**: 支持多种格式转换（SRT → TXT → HTML）
- 🔄 **双语合并**: 将翻译后的文本与原字幕时间轴合并生成双语字幕
- ⚙️ **精细调整**: 提供字幕位置微调功能，确保翻译准确性
- 📊 **可视化预览**: 生成HTML格式便于翻译校对

## 项目结构

```
subtitle_translation/
├── chinese/           # 原始中文字幕文件目录
├── middle_cn/         # 提取的中文字幕文本目录
├── middle_en/         # 翻译后的英文字幕文本目录
├── english/           # 最终生成的双语字幕目录
├── html/              # HTML格式预览文件目录
├── util/              # 核心工具模块
│   └── split_chinese_subtitle.py
├── main.ipynb         # 主要使用流程（Jupyter Notebook）
├── main.py            # 程序入口
└── pyproject.toml     # 项目配置文件
```

## 安装要求

- Python 3.10 或更高版本
- Jupyter Notebook 环境（推荐）

## 快速开始

### 1. 准备工作

将需要翻译的 `.srt` 中文字幕文件放置在 `chinese/` 目录下。

### 2. 使用流程

#### 方法一：使用 Jupyter Notebook（推荐）

1. 打开 `main.ipynb` 文件
2. 修改文件名变量：
   ```python
   file_name = "你的字幕文件名"  # 不包含 .srt 扩展名
   ```
3. 按顺序执行以下代码块：

**第一步：预处理**

```python
# 提取中文字幕文本并生成HTML预览
extract_srt_text(input_file_path, middle_cn_path)
srt_to_html(input_file_path, html_file_path)
```

**第二步：人工翻译**

- 打开生成的HTML文件进行翻译
- 将翻译结果复制到 `middle_en/` 目录下的对应 `.txt` 文件中

**第三步：合并生成**

```python
# 合并生成最终的双语字幕
merge_subtitles(input_file_path, middle_en_path, result_file_path)
```

#### 方法二：命令行使用

```bash
python main.py
```

### 3. 高级功能

如需调整字幕显示位置，可使用：

```python
# 调整指定范围内的英文字幕位置
shift_english_subtitles(result_file_path, start_block, end_block)
```

## 核心函数说明

### extract_srt_text()

从SRT文件中提取纯文本内容

- **参数**: `srt_file_path`, `output_file_path`
- **功能**: 移除时间轴和序号，提取纯文本并用'|'连接

### merge_subtitles()

合并中英文内容生成双语字幕

- **参数**: `chinese_srt_path`, `english_txt_path`, `output_srt_path`
- **功能**: 保持原有时间轴，在每条中文字幕后添加对应英文翻译

### srt_to_html()

生成HTML格式预览文件

- **参数**: `srt_file_path`, `html_file_path`
- **功能**: 转换为网页格式便于翻译和校对

### shift_english_subtitles()

调整英文字幕显示位置

- **参数**: `srt_file_path`, `start`, `end`
- **功能**: 在指定字幕块范围内调整英文显示位置

## 使用示例

假设你要翻译名为"example_video.srt"的字幕文件：

1. 将文件放入 `chinese/example_video.srt`
2. 在notebook中设置 `file_name = "example_video"`
3. 执行预处理步骤
4. 翻译 `middle_cn/example_video.txt` 的内容到 `middle_en/example_video.txt`
5. 执行合并步骤
6. 最终结果保存在 `english/example_video_en.srt`

## 注意事项

- 确保中英文句子数量完全匹配
- 翻译时保持原有的句子顺序
- 时间轴信息会自动保留，无需手动处理
- 如遇格式问题，可使用位置调整功能进行微调

## 许可证

MIT License
