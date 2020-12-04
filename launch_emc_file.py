import subprocess
cmd = 'floating.sh nohup emacsclient --create-frame $FILE > /dev/null &'.split()
if __name__ == '__main__':
    subprocess.run(cmd)
