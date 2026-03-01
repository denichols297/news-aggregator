import os
import re

def load_shell_env():
    home = os.path.expanduser("~")
    for rc_file in [".zshrc", ".bashrc", ".bash_profile", ".profile", ".zprofile"]:
        rc_path = os.path.join(home, rc_file)
        if os.path.exists(rc_path):
            try:
                with open(rc_path, 'r') as f:
                    content = f.read()
                    print(f"Reading {rc_path}")
                    match = re.search(r'export\s+GEMINI_API_KEY\s*=\s*["\']?([^"\'\n]+)["\']?', content)
                    if match:
                        os.environ["GEMINI_API_KEY"] = match.group(1)
                        print(f"Loaded GEMINI_API_KEY from {rc_path}")
                        return
            except Exception as e:
                pass
load_shell_env()
print("API KEY:", bool(os.environ.get("GEMINI_API_KEY")))
