from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    send_file
)

from app.services.importers import DataImporter
from app.services.pipeline import DataPipeline
from app.services.profiler import DataProfiler
from app.services.exporters import DataExporter
from app.services.quality import DataQualityAnalyzer

main = Blueprint(
    'main',
    __name__
)


@main.route('/')
def home():

    return render_template(
        'index.html'
    )


@main.route(
    '/upload',
    methods=['POST']
)
def upload():

    file = request.files['file']

    path = f'uploads/{file.filename}'

    file.save(path)

    # =====================
    # IMPORTAÇÃO
    # =====================

    if file.filename.endswith('.csv'):

        df = DataImporter.csv(path)

    elif file.filename.endswith('.xlsx'):

        df = DataImporter.excel(path)

    else:

        return jsonify({

            'error':
            'Formato inválido'

        }), 400

    # =====================
    # PROFILING
    # =====================

    profile = DataProfiler.analyze(
        df
    )

    # =====================
    # PIPELINE
    # =====================

    pipeline = DataPipeline(df)

    result = pipeline.execute()

    cleaned_df = result[
        'dataframe'
    ]

    history = result[
        'history'
    ]

    # =====================
    # QUALIDADE
    # =====================

    quality_report = (
        DataQualityAnalyzer.analyze(
            cleaned_df
        )
    )

    # =====================
    # EXPORTAÇÕES
    # =====================

    DataExporter.csv(

        cleaned_df,

        'exports/cleaned_data.csv'
    )

    DataExporter.excel(

        cleaned_df,

        'exports/cleaned_data.xlsx'
    )

    DataExporter.parquet(

        cleaned_df,

        'exports/cleaned_data.parquet'
    )

    DataExporter.sql_file(

        cleaned_df,

        'exports/cleaned_data.sql'
    )

    # =====================
    # PREVIEW
    # =====================

    preview_data = (
        cleaned_df
        .head(10)
        .to_dict(
            orient='records'
        )
    )

    return jsonify({

        'message':
            'Arquivo processado com sucesso',

        'profile':
            profile,

        'quality':
            quality_report,

        'preview':
            preview_data,

        'history':
            history,

        'exports': {

            'csv':
                '/download/csv',

            'excel':
                '/download/excel',

            'parquet':
                '/download/parquet',

            'sql':
                '/download/sql'
        }
    })


# ==================================
# DOWNLOAD CSV
# ==================================

@main.route('/download/csv')
def download_csv():

    return send_file(

        'exports/cleaned_data.csv',

        as_attachment=True,

        download_name='cleaned_data.csv'
    )


# ==================================
# DOWNLOAD EXCEL
# ==================================

@main.route('/download/excel')
def download_excel():

    return send_file(

        'exports/cleaned_data.xlsx',

        as_attachment=True,

        download_name='cleaned_data.xlsx'
    )


# ==================================
# DOWNLOAD PARQUET
# ==================================

@main.route('/download/parquet')
def download_parquet():

    return send_file(

        'exports/cleaned_data.parquet',

        as_attachment=True,

        download_name='cleaned_data.parquet'
    )


# ==================================
# DOWNLOAD SQL
# ==================================

@main.route('/download/sql')
def download_sql():

    return send_file(

        'exports/cleaned_data.sql',

        as_attachment=True,

        download_name='cleaned_data.sql'
    )