import os
import sys

def set_project_root_as_cwd():
  project_root = os.path.dirname(os.path.abspath(sys.argv[0]))
  current_working_directory = os.getcwd()
  if current_working_directory != project_root:
    os.chdir(project_root)
    print(f"Текущий рабочий каталог изменён на: {os.getcwd()}")
  else:
    print(f"Текущий рабочий каталог совпадает с корневой папкой проекта: {current_working_directory}")

  