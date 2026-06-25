with open('templates/product.arm-wrestling-trainer.json', 'r') as f:
    lines = f.readlines()

# Find boundaries
start = None
end = None
for i, line in enumerate(lines):
    if '"trust_badges_section": {' in line:
        start = i
    if start is not None and '"main": {' in line:
        end = i
        break

print(f"trust_badges_section: lines {start+1}-{end} ({end-start} lines)")

# Delete trust_badges_section
del lines[start:end]

# Remove from order
new_lines = []
for line in lines:
    if '"trust_badges_section",' not in line:
        new_lines.append(line)
    else:
        # Fix trailing comma on previous line
        prev = new_lines[-1].rstrip()
        if prev.endswith(','):
            new_lines[-1] = prev[:-1] + '\n'
        print("Removed from order")

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
    print(f'✅ All match. {len(sec_keys)} sections')
print('Done!')
