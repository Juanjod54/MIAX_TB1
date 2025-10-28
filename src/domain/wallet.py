from datetime import date
from jinja2 import Template
from importlib import resources
from src.domain.data_class import DataClass


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

    def __plot_wallet_performance__(self):
        resampled = []
        lowest_interval = None

        for data_class in self.data_classes:
            if lowest_interval is None or data_class.interval.value < lowest_interval.value:
                lowest_interval = data_class.interval
        for data_class in self.data_classes:
            resampled.append(data_class.resample(lowest_interval))

        return DataClass.plot_field('Wallet\'s Performance', resampled, [DataClass.Field.PERFORMANCE], 'Performance')

    def __plots_report__(self):
        plots = {}
        for data_class in self.data_classes:
            plots[data_class] = data_class.plots_report()

        return plots

    def report(self, output_filename: str):
        """
        Generate a wallet report, displaying the statistics for each queried symbol
        :param output_filename: Output file's name
        :return: This method does not return anything
        """
        template_content = ""
        plots = self.__plots_report__()
        wallet_performance_plot = self.__plot_wallet_performance__()
        with resources.files("src.resources").joinpath(Wallet.TEMPLATE_FILENAME).open("r", encoding="utf-8") as f:
            template_content = f.read()

        rendered_content = Template(template_content).render(
            plots=plots,
            DataClass=DataClass,
            date=date.today().isoformat(),
            data_classes=self.data_classes,
            wallet_performance_plot=wallet_performance_plot
        )

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
