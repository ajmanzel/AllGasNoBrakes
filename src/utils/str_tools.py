def escaped_html(s: str):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
