import os
import signal
import subprocess

if __name__ == "__main__":
    python_process = None
    node_process = None

    def kill_process(pid: int):
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except:
            pass

    try:
        python_process = subprocess.Popen(
            ["pipenv", "run", "serve"],
            stderr=subprocess.STDOUT,
        )

        node_process = subprocess.Popen(
            ["yarn", "dev"],
            stderr=subprocess.STDOUT,
        )

        python_process.wait()
        kill_process(node_process.pid)

    except:
        if python_process:
            python_process.terminate()
        kill_process(python_process.pid)

        if node_process:
            node_process.terminate()
        kill_process(node_process.pid)
