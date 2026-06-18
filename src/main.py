
import os
import shutil
from textnode import TextNode, TextType

def setup_destination(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)

def copy_directory_contents(source, destination):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)
        if os.path.isdir(source_item):
            os.makedirs(destination_item)
            copy_directory_contents(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)
            print(f"Copied {source_item} to {destination_item}")
        

def main():
    source = "./static"
    destination = "./public"
    setup_destination(destination)
    copy_directory_contents(source, destination)

if __name__ == "__main__":    main()
