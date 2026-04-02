import os
import markdown
import frontmatter

MD_EXTENSIONS = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.tables',
    'markdown.extensions.attr_list',
    'markdown.extensions.sane_lists',
    'markdown.extensions.nl2br',
    'pymdownx.tasklist',
    'pymdownx.mark'
]

def reduce_line_spaces(text):
    return text.replace('\n\n\n', '\n')

def parse_markdown_file(filepath):
    if not os.path.exists(filepath):
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    html_content = md.convert(post.content)
    
    return {
        'metadata': post.metadata,
        'html': html_content,
        'raw_content': reduce_line_spaces(post.content)
    }
