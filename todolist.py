import json, sys, os, time


JSON_FILE = 'todo.json'
KEYS = ('id','title','description','status','time created','time last updated')
STATUS = ('TODO','IN PROGRESS','DONE')

def load_file():
  if not os.path.exists(JSON_FILE):
    with open(JSON_FILE,'w') as file:
      json.dump([],file)
  with open(JSON_FILE,'r') as file:
    try: 
      return json.load(file)
    except json.JSONDecodeError():
      return []

def save_to_file(tasks):
  with open(JSON_FILE,'w') as file:
    json.dump(tasks,file,indent=2)

def find_tasks(key,index):
  task_list = []
  tasks=load_file()
  if key.upper() == 'NONE': 
    if index.upper() == 'ALL':
      return tasks
    else: 
      print('This index does not exist')
      return 'NO KEY OR INDEX'
  elif key in KEYS: 
    for task in tasks:
      if index == task[key]: task_list.append(task)
      elif index in task[key] and key in KEYS[4:5]: task_list.append(task)
      else: 
        print('This index does not exist')
        return 'NO KEY OR INDEX'
    return task_list
  else: 
    print('This key does not exist')
    return 'NO KEY OR INDEX'

def add_to_file(title,description):
  tasks = load_file()
  task_id = max([task['id'] for task in tasks],default=-1) + 1
  time_created = time.asctime( time.gmtime() )
  tasks.append( { 'id':task_id,'title':title,'description':description,'status':'TODO','time created':time_created,'time last updated':'None' } )
  save_to_file(tasks)

def delete_from_file(key,index):
  tasks = load_file()
  delete_list = find_tasks(key,index)
  if delete_list == 'NO KEY OR INDEX':
    return
  else: 
    for task in delete_list:
      tasks.remove(task)
  save_to_file(tasks)

def update_task_description(id,description):
  pass

def change_task_status(id,status):
  pass



command = sys.argv
print(command)

match command[1].lower():
  case 'add': add_to_file( command[2],command[3] )
  case 'delete': delete_from_file( command[2],command[3] )
  case 'info': 
    print('\n Keys: id, title, description, status, time created, time last updated',
          '\n Status: todo, in progress, done',
          '\n\n -COMMANDS-'
          '\n add "title" "description" ',
          '\n delete "key" "index" ',
          '\n update "id" "decription" ',
          '\n mark ""',
          '\n list',
          '\n')
  case other: print('This command does not exist')

print(load_file())