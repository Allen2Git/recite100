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

def main():
    content = """ """
    # 读取 Markdown 文件
    with open('input_file.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into sections
    sections = content.split('\n\n# Sentence ')
    sections = [f'# Sentence {section}' for section in sections[1:]]

    j = 1
    # Process each section
    for section in sections:
        lines = section.split('\n')
        sentence = lines[0][12:]  # Extract the sentence
        paragraph_start = [i for i, line in enumerate(lines) if line.startswith('## paragraph:')][0]
        paragraph = '\n'.join(lines[paragraph_start + 1:paragraph_start + 2])  # Extract the paragraph
        words_start = [i for i, line in enumerate(lines) if line.startswith('## Words:')][0]
        words = ', '.join(lines[words_start + 1].split(', '))  # Extract the word list
        

        file_name = f"section_{j}"
        ## text_content = "sentence" + str(i) + '<break time="600ms"/>' + sentence + '<break time="600ms"/>' + paragraph[:4000] + '<break time="1s"/>' + 'Words <break time="1s"/>' + words[:1000]
        text_content = """sentence {i} <break time="600ms"/>
            {sentence}<break time="600ms"/>
            {paragraph}<break time="1s"/>
            Words <break time="1s"/>
            {words}""".format(i=j, sentence=sentence, paragraph=paragraph, words=words)

    
        # 替换换行符为SSML换行标签
        ssml_string = text_content.replace("\n", "")
        
        text = '<speak><prosody rate="90%"> ' + ssml_string + "</prosody></speak>"
        # 生成句子的语音文件
        generate_audio(f"{text}", file_name)

        j = j + 1

if __name__ == '__main__':
    main()