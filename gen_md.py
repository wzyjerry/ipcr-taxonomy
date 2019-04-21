from lxml import etree
import xmltodict

def get_core_en_root(filename):
    doc = etree.parse(filename)
    root = doc.xpath('/revisionPeriods/revisionPeriod/ipcEdition[@ipcLevel="c"]/en/staticIpc')
    return root[0]

def get_A99AZZZMGGZZZZ(text):
    if len(text) <= 4:
        return text
    elif len(text) == 14:
        A = text[:4]
        B = text[4:8].lstrip('0')
        C = text[8:].rstrip('0')
        if len(C) == 0:
            C = '00'
        elif len(C) == 1:
            C = '%s0' % C
        return '%s %s/%s' % (A, B, C)
    else:
        pass

def get_sref(elem):
    ref = elem.get('ref')
    return ref

def get_mref(elem):
    ref = elem.get('ref')
    end_ref = elem.get('endRef')
    return ref, end_ref

def get_img(elem):
    return elem.get('src')

def get_sub(elem):
    return elem.text

def get_sup(elem):
    return elem.text

def resolve_tag(elem, l):
    if elem.tag == 'nbsp':
        l.append('&nbsp;')
    elif elem.tag == 'img':
        src = get_img(elem)
        l.append('![%s](%s)' % (src, src))
    elif elem.tag == 'sub':
        l.append('<sub>%s</sub>' % get_sub(elem))
    elif elem.tag == 'sup':
        l.append('<sup>%s</sup>' % get_sup(elem))
    elif elem.tag == 'degree':
        l.append('°')
    elif elem.tag == 'dbond':
        l.append('=')
    elif elem.tag == 'tbond':
        l.append('≡')
    elif elem.tag == 'larrow':
        l.append('←')
    elif elem.tag == 'rarrow':
        l.append('→')
    elif elem.tag == 'llinkt':
        l.append('〉')
    elif elem.tag == 'rlinkt':
        l.append('〈')
    elif elem.tag == 'llinkthree':
        l.append('![llinkthree.gif](llinkthree.gif)')
    elif elem.tag == 'ge':
        l.append('≥')
    elif elem.tag == 'u':
        l.append('<u>%s</u>' % get_u(elem))
    elif elem.tag == 'emdash':
        l.append('—')
    elif elem.tag == 'endash':
        l.append('–')
    elif elem.tag == 'sref':
        l.append(get_A99AZZZMGGZZZZ(get_sref(elem)))
    elif elem.tag == 'mref':
        ref, end_ref = get_mref(elem)
        l.append('%s to %s' % (get_A99AZZZMGGZZZZ(ref), get_A99AZZZMGGZZZZ(end_ref)))
    elif elem.tag == 'beta':
        l.append('β')
    else:
        print('get_text unknown tag: ', sub.tag)


def get_text(elem_text):
    text = []
    if elem_text.text:
        text.append(elem_text.text)
    for sub in elem_text:
        resolve_tag(sub, text)
        if sub.tail:
            text.append(sub.tail)
    return ''.join(text).strip()

def cut_for_subclass_index(ref):
    B = ref[4:8].lstrip('0')
    return '%s/00' % B

def cut_for_group(ref):
    B = ref[4:8].lstrip('0')
    C = ref[8:].rstrip('0')
    if len(C) == 0:
        C = '00'
    elif len(C) == 1:
        C = '%s0' % C
    return '%s/%s' % (B, C)

def get_u(u):
    return u.text

def get_entry_reference(elem):
    text = []
    if elem.text:
        text.append(elem.text)
    for sub in elem:
        resolve_tag(sub, text)
        if sub.tail:
            text.append(sub.tail)
    return ''.join(text)

def get_title(elem):
    text = []
    for titlePart in elem.xpath('titlePart'):
        part = []
        ref = []
        for item in titlePart:
            if item.tag == 'text':
                part.append(get_text(item))
            elif item.tag == 'entryReference':
                ref.append(get_entry_reference(item))
        if len(ref):
            part.append(' (')
            part.append('; '.join(ref))
            part.append(')')
        text.append(''.join(part))
    return '; '.join(text)

def get_references(elem):
    text = []
    if elem.text:
        text.append(elem.text)
    for sub in elem:
        if sub.tag == 'sref':
            ref = get_sref(sub)
            text.append(cut_for_subclass_index(ref))
        elif sub.tag == 'mref':
            ref, end_ref = get_mref(sub)
            text.append('%s to %s' % (cut_for_subclass_index(ref), cut_for_subclass_index(end_ref)))
        else:
            print('get_references unknown tag: ', sub.tag)
        if sub.tail:
            text.append(sub.tail)
    return ''.join(text).strip()

def get_index(elem):
    index = {}
    for item in elem:
        if item.tag == 'text':
            index['text'] = get_text(item)
        elif item.tag == 'references':
            index['references'] = get_references(item)
        elif item.tag == 'indexEntry':
            index.setdefault('children', [])
            index['children'].append(get_index(item))
    return index

def get_subnote_references(elem):
    A = []
    B = []
    C = []
    first = True
    def append_to_AB(ref):
        ref = get_A99AZZZMGGZZZZ(ref).split()
        A.append(ref[0])
        if len(ref) > 1:
            B.append(ref[1])
        else:
            B.append('')
    for sub in elem:
        if sub.tag == 'sref':
            ref = get_sref(sub)
            append_to_AB(ref)
            if first:
                first = False
            else:
                C.append(',')
        elif sub.tag == 'mref':
            ref, end_ref = get_mref(sub)
            append_to_AB(ref)
            append_to_AB(end_ref)
            if first:
                first = False
            else:
                C.append(',')
            C.append('to')
        else:
            print('get_subnote_references unknown tag:', sub.tag)
    C.append('&nbsp;')
    C = '<br>'.join(C)
    if B[0] != '':
        return '<br>'.join(A), '<br>'.join(B), C
    else:
        return '<br>'.join(A), C, ''

def get_subnote(elem, ind):
    text = []
    t = elem.get('type')
    if t == 'table':
        text.append('> |||||')
        text.append('> |:---|:---:|---:|:---|')
    for noteParagraph in elem.xpath('noteParagraph'):
        part = []
        ref = False
        for sub in noteParagraph:
            if sub.tag == 'text':
                if ref:
                    part.append('%s|' % get_text(sub))
                else:
                    part.append('%s- %s' % ('\t' * ind, get_text(sub)))
            elif sub.tag == 'subnote':
                part.append('\n')
                part.append(get_subnote(sub, ind + 1))
            elif sub.tag == 'orphan':
                part.append(get_orphan(sub, ind + 1))
            elif sub.tag == 'references':
                part.append('> |%s|%s|%s|' % get_subnote_references(sub))
                ref = True
            else:
                print('get_subnote unknown tag:', sub.tag)
        text.append(''.join(part))
    return '\n'.join(text)

def get_orphan(elem, ind):
    part = []
    for sub in elem:
        if sub.tag == 'text':
            part.append(get_text(sub))
        elif sub.tag == 'subnote':
            part.append(get_subnote(sub, ind + 1))
        else:
            print('get_orphan unknown tag:', sub.tag)
    return '\n'.join(part)

def get_note(elem):
    text = []
    noteParagraphs = elem.xpath('noteParagraph')
    count = 0
    for noteParagraph in noteParagraphs:
        part = []
        for sub in noteParagraph:
            if sub.tag == 'text':
                part.append(get_text(sub))
            elif sub.tag == 'subnote':
                if len(noteParagraphs) > 1:
                    part.append(get_subnote(sub, 2))
                else:
                    part.append(get_subnote(sub, 1))
            elif sub.tag == 'orphan':
                part[-1] = '%s%s' % (part[-1], get_orphan(sub, 2))
            else:
                print('get_note unknown tag:', sub.tag)
        if len(noteParagraphs) > 1:
            count += 1
            text.append('%d. %s' % (count, '\n'.join(part)))
        else:
            text.append('%s' % '\n'.join(part))
    return '\n'.join(text)

def construct_ipcr(elem):
    kind, symbol, entryType = map(elem.get, ['kind', 'symbol', 'entryType'])
    node = {
        'kind': kind,
        'symbol': symbol,
        'entryType': entryType
    }
    if entryType == 'I':
        pass
    elif entryType == 'K':
        textBody = elem.find('textBody')
        if kind in ['s', 't', 'c', 'u', 'g', 'm', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']:
            title = textBody.find('title')
            node['title'] = get_title(title)
        elif kind == 'i':
            index = textBody.find('index')
            node['index'] = get_index(index)
        elif kind == 'n':
            note = textBody.find('note')
            node['note'] = get_note(note)
        elif kind == 'l':
            pass
        else:
            print('construct_ipcr unknown kind:', kind)
    else:
        # print('Unknown entry type:', entryType)
        pass
    ipcEntry = elem.xpath('./ipcEntry')
    if len(ipcEntry):
        node['children'] = []
        for child in elem.xpath('./ipcEntry'):
            node['children'].append(construct_ipcr(child))
    return node

def output_index(index, lv):
    text = []
    if 'text' in index:
        if 'references' in index:
            text.append('%s+ %s\t\t%s' % ('\t' * lv, index['text'], index['references']))
        else:
            text.append('%s+ %s' % ('\t' * lv, index['text']))
    if 'children' in index:
        for child in index['children']:
            text.append(output_index(child, lv + 1))
    return '\n'.join(text)
        
def output_md(node):
    text = []
    kind = node['kind']
    symbol = node['symbol']
    if 'title' in node:
        title = node['title']
        lc = title.find(' (')
    if kind == 's':
        text.append('# **%s**' % node['title'])
    elif kind == 't':
        text.append('## **%s**' % node['title'])
    elif kind == 'c':
        if lc != -1:
            text.append('## **%s %s**%s' % (symbol, title[:lc], title[lc:]))
        else:
            text.append('## **%s %s**' % (symbol, title))
    elif kind == 'u':
        text.append('***')
        if lc != -1:
            text.append('### **%s %s**%s' % (symbol, title[:lc], title[lc:]))
        else:
            text.append('### **%s %s**' % (symbol, title))
    elif kind == 'i':
        text.append('### <u>**Subclass Index**</u>')
        text.append(output_index(node['index'], -1))
        text.append('***')
    elif kind == 'm':
        if lc != -1:
            text.append('### **%s %s**%s' % (cut_for_group(symbol), title[:lc], title[lc:]))
        else:
            text.append('### **%s %s**' % (cut_for_group(symbol), title))
    elif kind == 'g':
        if lc != -1:
            text.append('### <u>**%s**</u>%s' % (title[:lc], title[lc:]))
        else:
            text.append('### <u>**%s**</u>' % title)
    elif kind in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B']:
        dot = int(kind, 16)
        text.append('### %s %s%s' % (cut_for_group(symbol), '. ' * dot, title))
    elif kind == 'n':
        text.append('> ### <u>**Note**</u>')
        text.append('> %s' % '\n> '.join(node['note'].split('\n')))
    elif kind == 'l':
        text.append('***')
    if 'children' in node:
        for child in node['children']:
            result = output_md(child).strip()
            if result != '':
                text.append(result)

    return '\n'.join(text)
    

if __name__ == "__main__":
    filename = 'data/ipcr_scheme_20060101.xml'
    root = get_core_en_root(filename)
    for i in range(8):
        ipcr = construct_ipcr(root[i])
        with open('data/md/%s.md' % chr(65 + i), 'w', encoding='utf-8') as fout:
            fout.write(output_md(ipcr))
