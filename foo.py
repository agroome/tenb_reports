from pathlib import Path
p = Path('.').glob('**/*.csv')

print(list(p))