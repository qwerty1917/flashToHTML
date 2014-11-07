import glob

gifs = glob.glob('*.gif')

html = open('index.html', 'r+')
source = html.read().decode('utf-8')
gif_html = ""

for index, gif in enumerate(gifs) :
    if not gif in source :
        gif_html += "<img src = \'" + gif + "\' class = \'gif-size gif-hidden\' id=\'" + "gif_" + str(index) + "\'/>\n"
    else :
        pass

source = source.replace('</div>', gif_html + "</div>")

html.truncate(0)
html.write(source)

print source