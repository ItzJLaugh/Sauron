import subprocess

result = subprocess.run(['sh', '-c', 'dmesg | tail -n 10'], capture_output=True, text=True)
print(result.stdout)

