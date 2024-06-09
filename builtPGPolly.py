import boto3
import re

# 创建 Polly 客户端
polly = boto3.client('polly')


# 定义一个函数来生成语音文件
def generate_audio(text, file_name):


    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        TextType='ssml',
        VoiceId='Ruth',
        Engine='long-form' #Valid Values: standard | neural | long-form | generative

    )

    file = open(f"{file_name}.mp3", "wb")
    file.write(response['AudioStream'].read())
    file.close()

def extract_sections(content):
    sections = []
    current_section = {}
    lines = content.split('\n')
    paragraph_lines = []

    for line in lines:
        if line.startswith('# Sentence'):
            if current_section:
                current_section['paragraph'] = '\n'.join(paragraph_lines)
                sections.append(current_section)
                current_section = {}
                paragraph_lines = []
            current_section['sentence'] = line.split('# Sentence ')[1]

        elif line.startswith('## paragraph:'):
            paragraph_lines = []

        elif line.startswith('## Words:'):
            current_section['paragraph'] = '\n'.join(paragraph_lines)
            current_section['words'] = line.split('## Words:')[1].strip()

        else:
            paragraph_lines.append(line)

    if current_section:
        current_section['paragraph'] = '\n'.join(paragraph_lines)
        sections.append(current_section)

    return sections

def main():
    content = ""
    # 读取 Markdown 文件
    with open('input_file.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用自定义函数提取标题、段落和单词列表
    sections = extract_sections(content)

    # 遍历匹配结果并生成语音文件
    for i, section in enumerate(sections, start=1):
        sentence = section['sentence']
        paragraph = section['paragraph']
        words = section['words']
        file_name = f"section_{i}"
        text_content = f"""sentence 
            {sentence}<break time="600ms"/>
            {paragraph}<break time="1s"/>
            Words <break time="1s"/>
            {words}"""

        # 替换换行符为SSML换行标签
        # ssml_string = text_content.replace("\n", "")
        # text = '<speak><prosody rate="90%"> ' + ssml_string + "</prosody></speak>"
        
        text = '<speak><prosody rate="90%"> ' + text_content + "</prosody></speak>"
        
        # 生成句子的语音文件
        generate_audio(f"{text}", file_name)
        print(f"{file_name}.mp3 generated")


def main_1():
    content = """ """
    # 读取 Markdown 文件
    with open('input_file.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式匹配标题、段落和单词列表
    #pattern = r'#\s*Sentence\s*\d+\n(.*?)##\s*paragraph:\n(.*?)##\s*Words:\n(.*?)(?=\n#\s*Sentence\s*\d+|$)'
    
    pattern = r'#\s*Sentence\s*\d+\n(.*?)##\s*paragraph:\n(.*?)\n(?:##\s*Words:\n(.*?)(?=\n#\s*Sentence\s*\d+\n|$)|$)'


    
    matches = re.findall(pattern, content, re.DOTALL)

    # 遍历匹配结果并生成语音文件
    for i, match in enumerate(matches, start=1):
        sentence, paragraph, words = match
        file_name = f"section_{i}"
        ## text_content = "sentence" + str(i) + '<break time="600ms"/>' + sentence + '<break time="600ms"/>' + paragraph[:4000] + '<break time="1s"/>' + 'Words <break time="1s"/>' + words[:1000]
        text_content = """sentence {i} <break time="600ms"/>
            {sentence}<break time="600ms"/>
            {paragraph}<break time="1s"/>
            Words <break time="1s"/>
            {words}""".format(i=i, sentence=sentence, paragraph=paragraph, words=words)

    
        # 替换换行符为SSML换行标签
        ssml_string = text_content.replace("\n", "")
        
        text = '<speak><prosody rate="90%"> ' + ssml_string + "</prosody></speak>"
        # 生成句子的语音文件
        generate_audio(f"{text}", file_name)
        print("{file_name}.mp3 generated".format(file_name=file_name))

if __name__ == '__main__':
    main()