import re

md_text = ["asdfasdflaw", "|asdf|asdfdf|asd|", "|:---:|---|---:|", "|a12s 3f|as123 123df|as12312d|", "|end| end2| end3|","|asd|","asdfasdflaw","|not a title|"]

def table(md_text):
    index = 0
    table_html = ''
    while index < len(md_text):
        if re.search(r'\|(.*\|)*', md_text[index]) is None:
            # this line is not the beginning with ||| format of a table
            index += 1
            continue
        elif index + 1 == len(md_text) or index + 2 == len(md_text) or \
        re.search(r'\|([:]?---[:]?\|)*', md_text[index + 1]) is None or \
        re.search(r'\|(.*\|)*', md_text[index + 2]) is None:
            # not enough line to support table
            index += 1
            continue
        else: # not the same length
            len_split_by_slash = len(md_text[index].split('|'))
            if len(md_text[index + 1 ].split('|')) != len_split_by_slash or \
            len(md_text[index + 2].split('|')) != len_split_by_slash:
                index += 1
                continue

            # find the range of the code
            end_index = index + 1
            while re.search(r'\|(.*\|)*', md_text[end_index]) and len_split_by_slash == len(md_text[end_index].split('|')):
                end_index += 1

            # print(md_text[index:end_index])

            table_html += '<table class="table table-bordered">'

            # table table format
            align_line = md_text[index + 1][1:len(md_text[index + 1]) - 1]
            # print(align_line)
            align = align_line.split('|')
            # print(align)
            for align_index in range(len(align)):
              if align[align_index][0] == ':' and align[align_index][-1] == ':':
                  align[align_index] = 'center'
              elif align[align_index][0] == ':':
                  align[align_index] = 'left'
              elif align[align_index][-1] == ':':
                  align[align_index] = 'right'
              else:
                  align[align_index] = 'center'
            # print(align)
            # title
            title = md_text[index][1:len(md_text[index]) - 1].split('|')
            table_html += '<thead><tr>'
            for i in range(len(title)):
                table_html += '<th scope="col" style="text-align:' + align[i] + ';">' + str(title[i]) + '</th>'
            table_html += '</tr></thead>'

            # contents
            table_html += '<tbody>'
            contents = md_text[index + 2:end_index]
            for content_line in contents:
                table_html += '<tr>'
                content_line = content_line[1:len(content_line) - 1].split('|')
                for i in range(len(content_line)):
                    table_html += '<td style="text-align:' + align[i] + ';">' + str(content_line[i]) + '</td>'
                table_html += '</tr>'

            table_html += '</tbody></table>'
            md_text = md_text[:index] + [table_html] + md_text[end_index:]
            # index = 0
            break
    return md_text
