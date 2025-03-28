import sys
import os
sys.path.append(os.path.abspath("external/myWord"))


from myword import tokenize_text
text = "ကျွန်တော်မြန်မာစာကို စမ်းသပ်နေပါတယ်။"
tokens = tokenize_text(text)
print(tokens)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(tokens)
