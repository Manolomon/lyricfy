import requests
from bs4 import BeautifulSoup
from guess_language import guess_language
page = requests.get('https://genius.com/Sufjan-stevens-visions-of-gideon-lyrics')
html = BeautifulSoup(page.text, 'html.parser')
lyrics = html.find('div', class_='lyrics').get_text()
print(lyrics)

"""
[Verse 1]
I have loved you for the last time
Is it a video? Is it a video?
I have touched you for the last time
Is it a video? Is it a video?

[Chorus]
For the love, for laughter, I flew up to your arms
Is it a video? Is it a video?
For the love, for laughter, I flew up to your arms
Is it a video? Is it a video?
Is it a video?

[Verse 2]
I have loved you for the last time
Visions of Gideon, visions of Gideon
And I have kissed you for the last time
Visions of Gideon, visions of Gideon

[Chorus]
For the love, for laughter, I flew up to your arms
Is it a video? (Is it a video?) Is it a video? (Is it a video?)
For the love, for laughter, I flew up to your arms
Is it a video? (Is it a video?) Is it a video? (Is it a video?)
For the love, for laughter, I flew up to your arms
Visions of Gideon, (visions of Gideon), visions of Gideon, (visions of Gideon)
For the love, for laughter, I flew up to your arms
Visions of Gideon, (visions of Gideon), visions of Gideon, (visions of Gideon), Visions of Gideon

[Outro]
Visions of Gideon, visions of Gideon, visions of Gideon
Visions of Gideon, visions of Gideon, visions of Gideon
Visions of Gideon, (Is it a video?), visions of Gideon, (Is it a video?), visions of Gideon
Visions of Gideon, (Is it a video?), visions of Gideon, (Is it a video?), visions of Gideon
(Is it a video?) (Is it a video?) (Is it a video?)
"""

guess_language(lyrics)
#'en'