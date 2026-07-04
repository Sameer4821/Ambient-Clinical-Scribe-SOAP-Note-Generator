class ICDService:

    ICD_DATABASE = {
        "viral infection": {
            "code": "B34.9",
            "description": "Viral infection, unspecified",
        },
        "flu": {
            "code": "J10.1",
            "description": "Influenza with respiratory manifestations",
        },
        "fever": {
            "code": "R50.9",
            "description": "Fever, unspecified",
        },
        "diabetes": {
            "code": "E11.9",
            "description": "Type 2 diabetes mellitus",
        },
        "hypertension": {
            "code": "I10",
            "description": "Essential hypertension",
        },
        "headache": {
            "code": "R51.9",
            "description": "Headache",
        },
    }

    @classmethod
    def recommend(cls, assessment: str):
        recommendations = []

        assessment = assessment.lower()

        for disease, icd in cls.ICD_DATABASE.items():
            if disease in assessment:
                recommendations.append(icd)

        return recommendations