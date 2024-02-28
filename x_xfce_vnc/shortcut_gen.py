import os
import json


def create_desktop_shortcut(application):
    desktop_shortcut_path = os.path.expanduser("~/Desktop/{}.desktop".format(application["Name"]))
    with open(desktop_shortcut_path, "w") as f:
        f.write("[Desktop Entry]\n")
        f.write("Name={}\n".format(application["Name"]))
        f.write("Exec={}\n".format(application["Config"]["Exec"]))
        f.write("Icon={}\n".format(application["Config"]["Icon"]))
        f.write("Type=Application\n")


def main():
    applications_json_path = os.environ.get("APPS_CONF")

    if not os.path.exists(applications_json_path):
        print("Apps config JSON file not found.")
        return

    with open(applications_json_path, "r") as f:
        applications = json.load(f)

    for application in applications["Apps"]:
        create_desktop_shortcut(application)

    print("Shortcuts created successfully.\n")


if __name__ == "__main__":
    main()
