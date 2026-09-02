import re
from datetime import datetime
from uuid import uuid4

from social_engineering_simulator.domain.email_template.entity import Template
from social_engineering_simulator.domain.email_template.services.exceptions import MissingVariableError, \
    EmptyVariableError
from social_engineering_simulator.domain.email_template.value_object import TemplateContext, SubjectText, \
    RenderedTemplate


class EngineTemplate:
    def __init__(self):
        self.token_pattern = re.compile(r'(\{\{.*?\}\}|\{%.*?%\}|[^{}]+)')

    def _tokenize(self, text: str) -> list[str]:
        rendered_result = []
        for match in self.token_pattern.findall(text):
            if match:
                rendered_result.append(match)

        return rendered_result

    def _render_tokens(self, tokens: list[str], context_template: TemplateContext) -> str:
        result_rendered = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if not token.startswith("{"):
                result_rendered.append(token)

            elif token.startswith("{{"):
                name = token.strip("{} ")
                try:
                    value = context_template.get(name)
                    if value is not None:
                        result_rendered.append(str(value))
                    else:
                        raise EmptyVariableError("The value cannot be empty.")
                except KeyError:
                    raise MissingVariableError(f"The variable {name} not found")

            elif token.strip().startswith('{% if'):
                condition = token.replace('{% if', '').replace('%}', '').strip()
                endif_index = self._find_closing_tag(tokens, i, 'if')
                try:
                    condition_value = context_template.get(condition)
                    if condition_value:
                        inner_tokens = tokens[i + 1:endif_index]
                        result_rendered.append(self._render_tokens(inner_tokens, context_template))
                except KeyError:
                    pass
                i = endif_index
            elif token.startswith('{% endif'):
                pass
            i += 1
        return ''.join(result_rendered)

    def _find_closing_tag(self, tokens: list[str], start: int, tag_type: str) -> int:
        depth = 1
        i = start + 1
        end_tag = f'{{% end{tag_type} %}}'
        while i < len(tokens) and depth > 0:
            token = tokens[i]
            if token.startswith(f'{{% {tag_type}'):
                depth += 1
            elif token.startswith(f'{{% end{tag_type}'):
                depth -= 1
                if depth == 0:
                    return i
            i += 1

        raise ValueError(f"Не найден закрывающий тег для {tag_type} на позиции {start}")

    def render(self, template: Template, context_template: TemplateContext) -> RenderedTemplate:

        tokens_content = self._tokenize(template.content.value)

        tokens_subject = self._tokenize(template.subject.value)

        content = self._render_tokens(tokens_content, context_template)

        subject = self._render_tokens(tokens_subject, context_template)

        return RenderedTemplate(subject=subject, content=content)


engine = EngineTemplate()
context = TemplateContext()
context.set("name", "John")
