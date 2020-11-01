from typing import List
from typing import Optional
from typing import Tuple

from pygments.lexers import get_lexer_for_filename


class Comment:
    def __init__(self):
        self.lines = []
        self.start = 1
        self.end = 1

    def append(self, other):
        self.lines.append(other)

    def __bool__(self):
        return bool(self.lines)

    @property
    def caption(self):
        return "\n".join(self.lines)


def parse(
    path: str, keep_comments: bool, start_line: int, end_line: Optional[int]
) -> Tuple[List[str], List[Comment]]:
    code: List[str] = []
    comments: List[Comment] = []
    lexer = get_lexer_for_filename(path)
    comment_marker = "#"
    if lexer.name in ("JavaScript", "Java", "C++"):
        comment_marker = "//"

    with open(path, "r") as f:
        comment = Comment()
        lines = f.readlines()[start_line - 1 :]

    if end_line and start_line - end_line < len(lines):
        lines = lines[: end_line - start_line + 1]
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"{comment_marker} end"):
            last_comment = comments[-1]
            last_comment.end = len(code)
            if not keep_comments:
                continue
        elif stripped.startswith(comment_marker):
            comment.append(stripped[2:].strip())
            if not keep_comments:
                continue
        elif comment:
            comment.start = len(code) + 1
            comment.end = comment.start
            comments.append(comment)
            comment = Comment()
        code.append(line)

    if not code[-1].strip():
        code = code[:-1]
    return code, comments
