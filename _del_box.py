with open('templates/product.arm-wrestling-trainer.json', 'r') as f:
    lines = f.readlines()

start = None
end = None
for i, line in enumerate(lines):
    if '"rich_text_CYKgjk": {' in line and start is None:
        start = i
    if start is not None and '"main": {' in line:
        end = i
        break

print(f"Deleting lines {start+1}-{end} ({end-start} lines)")

del lines[start:end]

# Remove from order
new_lines = []
for line in lines:
    if '"rich_text_CYKgjk",' in line or '"image_with_text_3nndy6",' in line:
        # Fix trailing comma on previous line
        prev = new_lines[-1].rstrip()
        if prev.endswith(','):
            new_lines[-1] = prev[:-1] + '\n'
        continue
    new_lines.append(line)

with open('templates/product.arm-wrestling-trainer.json', 'w') as f:
    f.writelines(new_lines)

# Validate
import re, json
with open('templates/product.arm-wrestling-trainer.json') as f:
    c = f.read()
no_comments = re.sub(r'/\*.*?\*/', '', c, flags=re.DOTALL)
d = json.loads(no_comments)
sec_keys = set(d['sections'].keys())
order_keys = set(d['order'])
diff1 = sec_keys - order_keys
diff2 = order_keys - sec_keys
if diff1:
    print(f'❌ In sections not in order: {diff1}')
elif diff2:
    print(f'❌ In order not in sections: {diff2}')
else:
    print(f'✅ {len(sec_keys)} sections, all match')
