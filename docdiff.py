import difflib
import re
import sys


def linediff(diff, start, end):
    new = []
    for seg in diff.split('\n'):
        if len(seg) > 0:
            new.append(start + seg + end)
        else:
            new.append('')
    return '\n'.join(new)


def strdiff(a, b):
    s = difflib.SequenceMatcher(
        a=a, b=b,
        isjunk=lambda x: x in ' \n',
        autojunk=False
    )
    new = ''
    a0 = 0
    b0 = 0
    for ai, bi, li in s.get_matching_blocks():
        if ai > a0:
            new += linediff(a[a0:ai], '[-', '-]')
        if bi > b0:
            new += linediff(b[b0:bi], '{+', '+}')
        new += a[ai:ai+li]
        a0 = ai + li
        b0 = bi + li
    return new


def splitdiff(a, b, addstyle, delstyle, newline):
    text = []
    delregex = re.compile('\\[-([^]]*)-\\]')
    addregex = re.compile('{\\+([^}]*)\\+}')
    for line in strdiff(a, b).split('\n'):
        del0 = line.find('[-')
        add0 = line.find('{+')
        if del0 >= 0 or add0 >= 0:
            old = delregex.sub(f'<span style="{delstyle}">\\1</span>', line)
            old = addregex.sub('', old)
            if len(old) > 0:
                text.append(old)
            new = addregex.sub(f'<span style="{addstyle}">\\1</span>', line)
            new = delregex.sub('', new)
            if len(new) > 0:
                text.append(new)
        else:
            text.append(line)
    return newline.join(text)


def htmldiff(a, b, fg, bg, ul):
    start = '''<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
'''
    addstyle = ''
    delstyle = ''
    if fg:
        addstyle += "color: blue;"
        delstyle += "color: red;"
    if bg:
        addstyle += "background-color: yellow;"
        delstyle += "background-color: yellow;"
    if ul:
        addstyle += "text-decoration-line: underline;"
        addstyle += "text-decoration-color: blue;"
        delstyle += "text-decoration-line: underline;"
        delstyle += "text-decoration-color: red;"
        delstyle += "text-decoration-style: wavy;"

    return start + splitdiff(a=a, b=b,
                             addstyle=addstyle,
                             delstyle=delstyle,
                             newline='<br>\n')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(htmldiff(open(sys.argv[1]).read(),
                       open(sys.argv[2]).read()))
    else:
        print('Please pass two plain text files as arguments')
else:
    from flask import Flask, request, send_file

    app = Flask('docdiff')

    @app.route('/')
    def index():
        return send_file('docdiff.html')

    @app.route('/result', methods=['POST', 'GET'])
    def process_file():
        return htmldiff(request.files['old'].read().decode(),
                        request.files['new'].read().decode(),
                        request.form.get('fg') == 'on',
                        request.form.get('bg') == 'on',
                        request.form.get('ul') == 'on')
