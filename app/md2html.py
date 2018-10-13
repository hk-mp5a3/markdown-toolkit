from app import app
from flask import request
from flask import jsonify
import json
from flask import render_template
import re


def check_paragraph(line):
    """ Check whether the line is paragraph, if it is, change it into html format


    :param line: str, a line in markdown file
    :return: str, the line in html format
    """
    if len(line) > 3 and line[:3] == '⋅⋅⋅':
        return '<p>' + line[3:] + '</p>'
    else:
        return line


def check_unordered_list(line):
    """ Check whether the line is unordered list, if it is, change it into html format

    :param line: str, a line in markdown file
    :return: boolean, whether a line is unordered list
             str, the line in html format
    """
    if line[:2] == '* ' or line[:2] == '- ' or line[:2] == '+ ' and len(line) > 2:
        return True, '<ul><li>' + line[2:] + '</li></ul>'
    return False, ''


def check_header(line):
    """ Check whether a line is header, if it is, change it into html format

    :param line: str, a line in markdown file
    :return: boolean, whether a line is header
             str, the line in html format
    """
    if line[:7] == '###### ':
        line = '<h6>' + line[7:] + '</h6>'
    elif line[:6] == '##### ':
        line = '<h5>' + line[6:] + '</h5>'
    elif line[:5] == '#### ':
        line = '<h4>' + line[5:] + '</h4>'
    elif line[:4] == '### ':
        line = '<h3>' + line[4:] + '</h3>'
    elif line[:3] == '## ':
        line = '<h2>' + line[3:] + '</h2>'
    elif line[:2] == '# ':
        line = '<h1>' + line[2:] + '</h1>'
    else:
        return False, ''

    return True, line


def contains_only_char(s, char):
    """ Check whether a str contains only one kind of char

    :param s: str, the string for checking
    :param char: str, the char for checking
    :return:
    """
    for c in s:
        if c != char:
            return False
    return True


def strong(line):
    """ Check if strong words exist, if exist, change it into html format

    :param line: str, the line in markdown format
    :return: str, the line in html format with strong style
    """
    if line.count('**') % 2 == 0:
        for i in range(0, line.count('**')):
            if i % 2 == 0:
                line = line.replace('**', '<strong>', 1)
            else:
                line = line.replace('**', '</strong>', 1)
    return line


def scratch(line):
    """ Check if scratch word exist, if exist, change it into html format

    :param line: str, the line in markdown format
    :return: str, the line in html format with scratch style
    """
    if line.count('~~') % 2 == 0:
        for i in range(0, line.count('~~')):
            if i % 2 == 0:
                line = line.replace('~~', '<del>', 1)
            else:
                line = line.replace('~~', '</del>', 1)
    return line


def italics(line):
    """ Check if italics word exist, if exist, change it into html format

    :param line: str, the line in markdown format
    :return: str, the line in html format with italics style
    """
    if line.count('__') % 2 == 0:
        for i in range(0, line.count('__')):
            if i % 2 == 0:
                line = line.replace('__', '<em>', 1)
            else:
                line = line.replace('__', '</em>', 1)
    return line


def check_horizontal_rule(line):
    """ Check if it is a horizontal rule, if exist, change it into html format

    :param line: str, the line in markdown format
    :return: boolean, whether it is a horizontal rule
             str, the line in html format for horizontal rule if it is
    """
    if line.count('-') >= 3 and contains_only_char(line, '-'):
        return True, '<hr></hr>'
    if line.count('*') >= 3 and contains_only_char(line, '*'):
        return True, '<hr></hr>'
    if line.count('_') >= 3 and contains_only_char(line, '_'):
        return True, '<hr></hr>'
    return False, ''


def convert(md_text):
    """ Convert markdown string to html format

    :param md_text: str, the markdown file
    :return: str, the html content
    """
    # separate by line
    md_text = md_text.split('\n')

    # save the html content for return
    html_text = ''

    # begin looping from the first line
    index = -1
    while index < len(md_text) - 1:
        index += 1
        line = md_text[index]

        # headers
        is_header, html_line = check_header(line)
        if is_header:
            html_text = html_text + html_line
            continue

        # horizontal rule
        is_horizontal_rule, html_line = check_horizontal_rule(line)
        if is_horizontal_rule:
            html_text = html_text + html_line
            continue

        # paragraph
        line = check_paragraph(line)

        # deal with ordered list
        if len(line.split('.')) != 0 and '1.' == line[:2]:
            html_line = '<ol>'
            order_index = index
            while order_index < len(md_text)\
                    and len(md_text[order_index].split('.')) != 0\
                    and (str(order_index - index + 1) == md_text[order_index].split('.')[0]
                         or '1' == md_text[order_index].split('.')[0]):
                to_replace = [str(order_index - index + 1) + '.', '1.']
                for replace_content in to_replace:
                    md_text[order_index] = md_text[order_index].replace(replace_content, '')
                html_line = html_line + '<li>' + md_text[order_index] + '</li>'

                order_index += 1
            index = order_index - 1
            html_line = html_line + '</ol>'
            line = html_line

        # code segment
        if len(line) >= 3 and line[:3] == '```':
            html_line = ""
            language = line[3:].replace(' ', '')
            order_index = index + 1
            find_end = False
            while order_index < len(md_text):
                if md_text[order_index][:3] == '```':
                    find_end = True
                    break
                else:
                    html_line += (md_text[order_index] + '<br/>')
                    order_index += 1

            if find_end:
                html_line = html_line.replace('<script', '&lt;script')
                html_line = html_line.replace('</script>', '&lt;/script&gt;')
                html_text += ('<code>' + html_line + '</code>')
                index = order_index
                continue

        # deal with unordered list
        is_unordered_list, html_line = check_unordered_list(line)
        if is_unordered_list:
            line = html_line

        # deal with strong
        line = strong(line)

        # Scratch
        line = scratch(line)

        # italics
        line = italics(line)

        # image
        while len(re.match(r'((?P<pre_text>.*)!\[(?P<alt_text>.*)\]\((?P<link>.*)\)(?P<after_text>.*))*', line).group())\
                != 0:
            match = re.match(r'((?P<pre_text>.*)!\[(?P<alt_text>.*)\]\((?P<link>.*)\)(?P<after_text>.*))*', line)
            pre_text = match.group('pre_text')
            alt_text = match.group('alt_text')
            link = match.group('link')
            after_text = match.group('after_text')
            img_html = '<img src="' + link + '" alt="' + alt_text + '">'
            line = pre_text + img_html + after_text

        # link
        while len(re.match(r'((?P<pre_text>.*)\[(?P<alt_text>.*)\]\((?P<link>.*)\)(?P<after_text>.*))*', line).group())\
                != 0:
            match = re.match(r'((?P<pre_text>.*)\[(?P<alt_text>.*)\]\((?P<link>.*)\)(?P<after_text>.*))*', line)
            pre_text = match.group('pre_text')
            alt_text = match.group('alt_text')
            link = match.group('link')
            after_text = match.group('after_text')
            img_html = '<a href="' + link + '">' + alt_text + '</a>'
            line = pre_text + img_html + after_text

        html_text = html_text + line
        if not is_unordered_list:
            html_text = html_text + '<br>'

    return html_text


@app.route('/md2html/', methods=["POST"])
def md2html():
    """ API for converting markdown to HTML

    Frontend uses it to send request. Get the string of markdown file.
    Call function to convert it into html format, and then return it as a response.

    :return: response, contains the text in HTML format
    """
    # Get the markdown text from the request
    data = json.loads(request.data)
    md_text = data['md_text']

    # Convert the markdown text to html format
    html_text = convert(md_text)

    # Generate response and send it to the front end
    response_dict = {"html_text": html_text}
    response = jsonify(response_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def index():
    """ Index page. Return the template.

    :return: template, the template of index html.
    """
    return render_template('index.html')
