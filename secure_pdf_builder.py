from fpdf import FPDF
import os
import traceback

class SafePDF(FPDF):
    def safe_text(self, text: str) -> str:
        """Convert text to latin-1 safe version, replacing invalid characters."""
        if not isinstance(text, str):
            text = str(text)
        return text.encode("latin-1", "replace").decode("latin-1")

    def safe_cell(self, *args, **kwargs):
        """Wrapper around cell() that handles encoding issues."""
        if "txt" in kwargs:
            kwargs["txt"] = self.safe_text(kwargs["txt"])
        return super().cell(*args, **kwargs)

    def safe_multi_cell(self, *args, **kwargs):
        """Wrapper around multi_cell() that handles encoding issues."""
        if "txt" in kwargs:
            kwargs["txt"] = self.safe_text(kwargs["txt"])
        return super().multi_cell(*args, **kwargs)

def genera_pdf(bandi_validi, output_path="report_bandi.pdf"):
    try:
        pdf = SafePDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        pdf.set_fill_color(200, 220, 255)
        pdf.set_text_color(0)
        pdf.set_draw_color(50, 50, 100)

        # Header
        pdf.set_font("Helvetica", "B", 14)
        pdf.safe_cell(0, 10, "Top 10 Bandi Consigliati", ln=True)

        # Column titles
        pdf.set_font("Helvetica", "B", 12)
        col_widths = [60, 60, 50, 20]
        headers = ["Titolo", "Obiettivo_Finalita", "Forma_agevolazione", "Punteggio"]
        for i, header in enumerate(headers):
            pdf.safe_cell(col_widths[i], 10, txt=header, border=1)
        pdf.ln()

        # Table rows
        pdf.set_font("Helvetica", "", 10)
        for row in bandi_validi:
            try:
                values = [row.get(h, "") for h in headers]
                for i, value in enumerate(values):
                    pdf.safe_cell(col_widths[i], 10, txt=str(value), border=1)
                pdf.ln()
            except Exception as row_err:
                pdf.set_text_color(255, 0, 0)
                pdf.safe_cell(0, 10, txt=f"Errore riga: {str(row_err)}", ln=True)
                pdf.set_text_color(0)

        # Save PDF
        pdf.output(output_path)
        return output_path

    except Exception as e:
        error_log_path = "pdf_generation_error.log"
        with open(error_log_path, "w") as f:
            f.write("Errore generazione PDF:\n")
            traceback.print_exc(file=f)
        return error_log_path
