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
  if key.upper() == 'SPEC': 
    if index.upper() == 'ALL':
      return tasks
    else: 
      print('This index does not exist')
      return 'NO KEY OR INDEX'
  elif key in KEYS: 
    for task in tasks:
      if index.lower() == str(task[key] ).lower(): task_list.append(task)
      elif index.lower() in str(task[key] ).lower() and key in KEYS[4:5]: task_list.append(task)
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
  tasks = load_file()
  new_task = find_tasks('id',id)
  if new_task == 'NO KEY OR INDEX':
    return
  new_task = new_task[0]
  new_task['description'] = description
  new_task['time last updated'] = time.asctime( time.gmtime() )
  for task in tasks:
    if task['id'] == new_task['id']: 
      tasks[tasks.index(task)] = new_task
  save_to_file(tasks)
  
def update_task_status(id,status):
  tasks = load_file()
  new_task = find_tasks('id',id)
  if new_task == 'NO KEY OR INDEX':
    return
  if status.upper() not in STATUS:
    print('This status is not suported')
    return
  new_task = new_task[0]
  new_task['status'] = status.upper()
  new_task['time last updated'] = time.asctime( time.gmtime() )
  for task in tasks:
    if task['id'] == new_task['id']: 
      tasks[tasks.index(task)] = new_task
  save_to_file(tasks)



command = sys.argv
print(command)

match command[1].lower():
  case 'add': add_to_file( command[2],command[3] )
  case 'delete': delete_from_file( command[2],command[3] )
  case 'update': update_task_description( command[2],command[3] )
  case 'mark': update_task_status( command[2],command[3] )
  case 'info': 
    print('\n Keys: id, title, description, status, time created, time last updated',
          '\n Special Key: spec | Special Index: all',
          '\n Status: todo, in progress, done',
          '\n\n -COMMANDS-'
          '\n add "title" "description" ',
          '\n delete "key" "index" ',
          '\n update "id" "decription" ',
          '\n mark "id" "status" ',
          '\n list "key" "index" ',
          '\n')
  case other: print('This command does not exist')

print(load_file())