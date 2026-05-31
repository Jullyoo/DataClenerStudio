class CleaningRules:

    DEFAULT_RULES = {

        'financial': [

            'clean_currency',

            'clean_dates',

            'remove_duplicates',

            'clean_nulls'
        ],

        'crm': [

            'clean_text',

            'remove_duplicates'
        ],

        'hr': [

            'clean_text',

            'clean_dates',

            'clean_nulls'
        ]
    }

    @staticmethod
    def get_rule(rule_name):

        return CleaningRules.DEFAULT_RULES.get(
            rule_name,
            []
        )