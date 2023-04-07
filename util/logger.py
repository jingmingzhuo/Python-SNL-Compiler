import time

DEBUG = False

def set_debug():
  global DEBUG
  DEBUG = True

def log(*values):
  if not DEBUG:
    return

  timeStr = time.time() // 5
  with open(f'log/{timeStr}.log', 'a', encoding='utf-8') as f:
    print(*values, file=f)