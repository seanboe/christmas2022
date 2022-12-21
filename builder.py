import re
from os import listdir
from os.path import isfile, join

base_path = '/Users/seanboerhout/Documents/webDev/testing-python/'
letters_path = 'letters/'
dist_path = 'dist/'

def main():

  layout_body_standard = ""
  layout_keywords = []
  with open(base_path + "letter-layout.html", "r") as layout:
    layout_body_standard = layout.read()
    layout_keywords = re.findall(r'{{(.*?)}}', layout_body_standard)
  
  letter_files = [f for f in listdir(base_path + letters_path) if isfile(join(base_path + letters_path, f))]

  for letter in letter_files:
    text_body = ""
    layout_body = layout_body_standard
    metadata = {}
    with open(base_path + letters_path + letter, "r") as text:
      text.readline()
      line = text.readline().strip()
      while line != "---":
        element = line.split(" ")
        metadata[str(element[0])[:-1]] = str(element[1])
        line = text.readline().strip()
      
      text_body = text.read()

    layout_body = layout_body.replace("{{text_body}}", text_body)
    for keyword in layout_keywords:
      if keyword == "text_body":
        continue
      try:
        layout_body =layout_body.replace("{{" + keyword + "}}", metadata[keyword])
      except:
        print(f"Error in building file \"{letter}\"")

    with open(base_path + dist_path + letter[:letter.find(".")] + ".html", "w") as dist_file:
      dist_file.write(layout_body)

    print("Build completed!")

if __name__ == "__main__":
  main()