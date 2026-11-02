#!/usr/bin/env python3
"""Compose '<name>-add.svg' (blue plus) and '<name>-load.svg' (green down arrow) from Tango base icons.

usage: make_icons.py <iconset scalable dir> <out dir> name=base [name=base ...]
Also writes '<name>.svg': the base itself at full size (no badge), cleaned the same way, so the whole
family shares one name prefix.
e.g.   make_icons.py scalable scalable bwfm-film=video bwfm-book=accessories-dictionary
A pair 'name=base+badge' (e.g. bwfm-author=dashboard-show+cs-user) writes only '<name>.svg': the base
with another icon, scaled to BADGE_ICON_SCALE, in its bottom-right corner.
Each base is scaled to SCALE and pinned top-left of a 48x48 canvas; the badge sits bottom-right.
Ids of the base are prefixed so two gradients never clash. Existing output files are overwritten.
"""
import re, sys
from lxml import etree

SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
SCALE = 0.84
BADGE_ICON_SCALE = 0.8

BADGES = {
    'add': '''
  <linearGradient id="badgeBlue" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#729fcf"/><stop offset="1" stop-color="#3465a4"/>
  </linearGradient>
  <path d="M31 24h10v7h7v10h-7v7h-10v-7h-7v-10h7z" transform="translate(-4 -4)"
        fill="url(#badgeBlue)" stroke="#204a87" stroke-width="1.4" stroke-linejoin="round"/>''',
    'load': '''
  <linearGradient id="badgeGreen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8ae234"/><stop offset="1" stop-color="#4e9a06"/>
  </linearGradient>
  <path d="M30 22h10v10h7l-12 14l-12-14h7z" transform="translate(-1 -1)"
        fill="url(#badgeGreen)" stroke="#2e6d06" stroke-width="1.4" stroke-linejoin="round"/>''',
}


def clean_base(path):
    tree = etree.parse(path)
    root = tree.getroot()
    for el in list(root.iter()):
        tag = etree.QName(el).localname if isinstance(el.tag, str) else None
        if tag in ('metadata', 'namedview'):
            el.getparent().remove(el)
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        for k in list(el.attrib):
            if k.split('}')[-1].startswith(('export-', 'docname', 'docbase', 'version', 'output_extension')) and '}' in k \
                    and not k.endswith('href'):
                del el.attrib[k]
    return root


def prefix_ids(root, prefix):
    ids = {el.get('id') for el in root.iter() if isinstance(el.tag, str) and el.get('id')}
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        for k, v in list(el.attrib.items()):
            nv = v
            if k == 'id' and v in ids:
                nv = prefix + v
            else:
                nv = re.sub(r'url\(#([^)]+)\)', lambda m: 'url(#%s%s)' % (prefix, m.group(1)) if m.group(1) in ids else m.group(0), nv)
                if k.endswith('href') and nv.startswith('#') and nv[1:] in ids:
                    nv = '#' + prefix + nv[1:]
            if nv != v:
                el.set(k, nv)
        if el.text and 'url(#' in el.text:  # <style> blocks
            el.text = re.sub(r'url\(#([^)]+)\)', lambda m: 'url(#%s%s)' % (prefix, m.group(1)), el.text)


def compose(src, kind, badge_src=None):
    root = clean_base(src)
    prefix = 'b_'
    prefix_ids(root, prefix)
    out = etree.Element('{%s}svg' % SVG, nsmap={None: SVG, 'xlink': XLINK, 'inkscape': 'http://www.inkscape.org/namespaces/inkscape', 'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'})
    out.set('width', '48')
    out.set('height', '48')
    out.set('viewBox', '0 0 48 48')
    g = etree.SubElement(out, '{%s}g' % SVG)
    if kind:
        g.set('transform', 'scale(%s)' % SCALE)
    for child in list(root):
        g.append(child)
    if badge_src:
        broot = clean_base(badge_src)
        prefix_ids(broot, 'k_')
        bg = etree.SubElement(out, '{%s}g' % SVG)
        bg.set('transform', 'translate(48 48) scale(%s) translate(-48 -48)' % BADGE_ICON_SCALE)
        for child in list(broot):
            bg.append(child)
    elif kind:
        badge = etree.fromstring('<g xmlns="%s" transform="translate(47 47) scale(0.8) translate(-47 -47)">%s</g>' % (SVG, BADGES[kind]))
        out.append(badge)
    return etree.tostring(out, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()


if __name__ == '__main__':
    srcdir, outdir, *pairs = sys.argv[1:]
    for pair in pairs:
        name, base = pair.split('=', 1)
        if '+' in base:
            base, badge = base.split('+', 1)
            with open('%s/%s.svg' % (outdir, name), 'w') as f:
                f.write(compose('%s/%s.svg' % (srcdir, base), None, '%s/%s.svg' % (srcdir, badge)))
            print('%s.svg' % name)
            continue
        for kind in (None, 'add', 'load'):
            out = '%s%s.svg' % (name, '-' + kind if kind else '')
            with open('%s/%s' % (outdir, out), 'w') as f:
                f.write(compose('%s/%s.svg' % (srcdir, base), kind))
            print(out)
