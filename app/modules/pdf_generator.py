import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer


class PDFGenerator:
    """
    Generates a clinical report PDF.
    """

    def generate(
        self,
        audio_id,
        transcript,
        soap,
        icd,
    ):

        os.makedirs(
            "reports",
            exist_ok=True,
        )

        filename = f"reports/{audio_id}.pdf"

        document = SimpleDocTemplate(
            filename,
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>Ambient Clinical Scribe Report</b>",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Transcript</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                transcript,
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>SOAP Note</b>",
                styles["Heading2"],
            )
        )

        for key, value in soap.items():

            story.append(
                Paragraph(
                    f"<b>{key.title()}</b>",
                    styles["Heading3"],
                )
            )

            story.append(
                Paragraph(
                    str(value),
                    styles["BodyText"],
                )
            )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "<b>ICD Recommendations</b>",
                styles["Heading2"],
            )
        )

        for recommendation in icd["recommendations"]:

            story.append(
                Paragraph(
                    f'{recommendation["code"]} - '
                    f'{recommendation["description"]} '
                    f'({recommendation["confidence"]}%)',
                    styles["BodyText"],
                )
            )

        document.build(
            story,
        )

        return filename