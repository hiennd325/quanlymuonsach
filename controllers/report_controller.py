"""
Report Controller — Điều phối dữ liệu phân tích và báo cáo
"""


class ReportController:
    def __init__(self, report_model):
        self.report_model = report_model

    def get_report_data(self):
        kpis = self.report_model.get_kpis()
        top_books = self.report_model.get_top_books(10)
        top_categories = self.report_model.get_top_categories(10)

        return {
            "kpis": kpis,
            "top_books": top_books,
            "top_categories": top_categories
        }
