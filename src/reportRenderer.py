from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ReportRenderer:
    """
    Class to generate static HTML report of data
    """

    def __init__(
        self,
        template_dir: str,
    ) -> None:

        # Set up Jinja2 Environment class
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render(self, template_name: str, context: dict, output_path: str) -> None:
        """
        Render a HTML report from our data
        """

        # Get the correct template for our data
        template = self.env.get_template(template_name)

        # Render the template to HTML using our variables (technical debt data)
        html = template.render(**context)

        # Create directories (if needed) and write to an output file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html, encoding="utf-8")
