#!/usr/bin/env python3
import argparse
import os
import re


class Converter:
    def __init__(self, filename=None, filestorage=None):
        self.regex_date = re.compile(r'—+\s+(\d{4}-\d{2}-\d{2})\s+—+')
        self.regex_person = re.compile(r'(\w+)\s+\d{2}:\d{2}')
        self.regex_article = re.compile(r'(\d+\.?\s*)?([-a-zA-Z0-9]+\d{4}[-&.0-9a-zA-Z]+)\s*(.*)')
        self.regex_comment = re.compile(r'(.+)')
        self.regex_datesimp = re.compile(r'.*(\d{2,4})\.?(\d{2})\.?(\d{2}).*')

        self.date, self.person, self.article_id, self.comment = '', '', '', ''
        self.article_comments = []

        if filename:
            self.rawlines = open(filename).readlines().split('\n')
        else:
            self.rawlines = filestorage.read().decode().split('\n')

        if os.path.exists('name_map.txt'):
            self.name_map = None

    def parse(self):
        for line in self.rawlines:
            line = line.strip()

            if len(line) == 0:
                continue
            elif ((line.find('文献') >= 0 and
                  (line.find('浏览') >= 0 or line.find('阅读') >= 0))):
                if (match_datesimp := self.regex_datesimp.match(line)):
                    datesimp = list(match_datesimp.groups())
                    if len(datesimp[0]) == 2:
                        datesimp[0] = '20' + datesimp[0]
                    self.date = '-'.join(datesimp)
            elif (match_date := self.regex_date.match(line)):
                self.date = match_date.groups()[0]
            elif (match_person := self.regex_person.match(line)):
                self.person = match_person.groups()[0]
            elif (match_article := self.regex_article.match(line)):
                dummy_index, self.article_id, self.comment = match_article.groups()
                self.article_comments.append({
                    "person": self.person,
                    "date": self.date,
                    "article_id": self.article_id,
                    "comment": self.comment,
                })
            elif (match_comment := self.regex_comment.match(line)):
                if len(self.article_comments) > 0:
                    comment = match_comment.groups()[0]
                    if len(self.article_comments[-1]['comment']) > 0:
                        self.article_comments[-1]['comment'] += '↵ '
                    self.article_comments[-1]['comment'] += comment
            else:
                print('Unmatched:', line)

    def export(self):
        with open(self.file + '.csv', 'w') as f:
            f.write('姓名\t日期\t文献\t备注\n')
            for i in self.article_comments:
                f.write('{person}\t{date}\t{article_id}\t{comment}\n'.format_map(i))
        print("Total number:", len(self.article_comments))

    def html_table(self):
        table = ['<table>']
        table.append('<tbody>')
        for i in self.article_comments:
            table.append('<tr>')
            for k in ['person', 'date', 'article_id', 'comment']:
                table.append(f"<td>{i[k]}</td>")
            table.append('</tr>')
        table.append('</tbody></table>')
        return '\n'.join(table)


def wrap_convert(request):
    request.files
    c = Converter(filestorage=request.files['raw'])
    c.parse()
    return '''<!DOCTYPE html> <html> <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="static/table.css" rel="stylesheet" />
    </head><body>{}</body></html>'''.format(c.html_table())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    if os.path.exists(args.file):
        self = Converter(args.file)
        self.parse()
        self.export()
    else:
        print('input file doesn\'t exist')
