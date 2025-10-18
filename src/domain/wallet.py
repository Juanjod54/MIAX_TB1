from datetime import date
from src.domain.data_class import DataClass
from jinja2 import Template
from importlib import resources

class Wallet:

    TEMPLATE_FILENAME = 'wallet_report_template.j2'

    def __init__(self):
        self.data_classes = []

    def add_data_classes(self, data_classes: list[DataClass]):
        """
        Adds a list of data classes to the wallet
        :param data_classes: list of the data classes
        :return: This method does not return anything
        """
        self.data_classes.extend(data_classes)

    def report(self, output_filename: str):
        """
        Generate a wallet report, displaying the statistics for each queried symbol
        :param output_filename: Output file's name
        :return: This method does not return anything
        """
        template_content = ""
        with resources.files("src.resources").joinpath(Wallet.TEMPLATE_FILENAME).open("r", encoding="utf-8") as f:
            template_content = f.read()

        rendered_content = Template(template_content).render(
            DataClass=DataClass,
            date=date.today().isoformat(),
            data_classes=self.data_classes
        )

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
