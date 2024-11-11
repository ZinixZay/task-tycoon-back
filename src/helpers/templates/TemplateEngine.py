import re


class TemplateEngine:

    @staticmethod
    def build_string(template: str, *args) -> str:
        template_args_amount = len(set(re.findall(r'\$\d', template)))

        if template_args_amount != len(args):
            raise TypeError('template and passed arguments are incompatible')
        
        filled_template = template
        for idx in range(1, template_args_amount + 1):
            filled_template = filled_template.replace('$' + str(idx), args[idx - 1])
        
        return filled_template
