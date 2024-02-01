import base64, json, os

from openai import OpenAI
from dotenv import load_dotenv

from DevOpsHandler import DevOpsHandler
from Formatter import Formatter
from ReportEmail import ReportEmail

with open('./credentials.json') as f:
    credentials = json.load(f)

#############################################
#            RETRIEVE WORK ITEMS            #
#############################################
encoded_pat = base64.b64encode(f":{credentials['AZURE_PAT']}".encode()).decode()

devOpsHandler = DevOpsHandler(organization=credentials['AZURE_ORG'],
                              project=credentials['AZURE_PROJECT'],
                              encoded_pat=encoded_pat)

work_item_IDs = devOpsHandler.getWorkItems(credentials['QUERY_ID'])
work_items = devOpsHandler.gatherWorkItemDescriptions(work_item_IDs)
num_work_items = str(len(work_items))

print(f"Retrieved {num_work_items} work items from Azure DevOps...")

#############################################
#              CALL OPENAI API              #
#############################################
print('Calling OpenAI API on work items...')

load_dotenv()

client = OpenAI()

with open('systemRole.txt') as f:
    system_context = f.read()

with open('systemRole.txt') as f:
    system_role = f.read()

with open('systemInput.txt') as f:
    system_task = f.read()

i = 0
for item in work_items:
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": system_task},
        {"role": "user", "content": system_role},
        {"role": "system", "content": system_task.format(title=item['Title'], description=item['Description'])}
      ]
    )
    item['Generated_note'] = completion.choices[0].message.content

    i += 1
    print(f"Work item {i}/{num_work_items} complete...")

# Low Token Cost Test for OpenAI API Connection 
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": 'Say one word'}
#   ]
# )

# print(completion.choices[0].message.content)

print('OpenAI API Calls Completed...')

#############################################
#                 FORMATTING                #
#############################################
formatter = Formatter()

for item in work_items:
    formatter.formatWorkItemNote(item)

final_HTML = formatter.returnHTML()

#############################################
#                 SEND EMAIL                #
#############################################
reportEmail = ReportEmail(sender_email=credentials['SENDER_EMAIL'],
                          password=credentials['SEND_APP_PASSWORD'],
                          recipients=credentials['RECIPIENTS'],
                          subject='Release Notes')

print('Sending email with Release Notes Content...')
reportEmail.create_message(final_HTML)
reportEmail.send_message()
print('Complete.')