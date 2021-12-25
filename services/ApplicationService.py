import subprocess
from pydantics.Application import AppOut


class ApplicationService:
    @staticmethod
    def get_all_apps():
        output = subprocess.run("sudo dpkg --get-selections", shell=True, capture_output=True, text=True).stdout
        output = output.splitlines()
        output = [AppOut(name=item.split("\t")[0]) for item in output]
        return output

    @staticmethod
    def remove_app(name: str):
        output = subprocess.run(f"sudo dpkg --purge {name}", shell=True, capture_output=True, text=True).stdout


