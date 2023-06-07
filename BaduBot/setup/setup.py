import os
import site
import shutil

site_packages_path = site.getsitepackages()[0]
confirmation = input("The file named 'tiv_config' will be moved to the location " + site_packages_path +
                     ".\nIf a file with the same name exists in the specified location, its contents will be deleted.\nDo you confirm? (Y/n)\nDefault input will be taken for invalid inputs (Y): ")

if confirmation.upper() != "N":
    source_file = os.path.join(os.getcwd(), "tiv_config.py")
    destination_file = os.path.join(site_packages_path, "tiv_config.py")
    shutil.copy2(source_file, destination_file)
