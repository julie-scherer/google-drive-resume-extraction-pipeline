from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# todo MODIFY THIS PART DEPENDING ON WHICH SOURCE YOURE READING FROM
input_file = 'data/resume_data.csv' # 'data/resume_data.json'
with open(input_file, 'r') as file:
    input_data = file.read()

out_folder = 'output'
os.makedirs(out_folder, exist_ok=True)

# todo DEFINE NAME OF OUTPUT FILE
out_file = 'output.md'
out_path = os.path.join(out_folder, out_file)
open(out_path, 'w').close()

# todo WRITE SYSTEM PROMPT
system_prompt = """

"""

# todo WRITE USER PROMPT
user_prompt = f"""

"""

print(system_prompt)
print(user_prompt)

response = client.chat.completions.create(model="gpt-4",
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
],
temperature=0)
answer = response.choices[0].message.content

if not os.path.exists('output'):
    os.mkdir('output')

with open(f'output/{out_file}', 'w') as file:
    file.write(answer)
