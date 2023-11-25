from app.models.charts import daily_artists, daily_tracks
from app.models.artist_catalog import artist_catalog

def daily_chart_joined_art_cat(
        chart_model,
        chart_date,
        ):
    results = chart_model.query.filter(
        chart_model.date == chart_date
        ).join(artist_catalog, chart_model.art_id==artist_catalog.art_id
        ).add_columns(
            artist_catalog.genre,
            artist_catalog.genre2, 
            artist_catalog.master_genre, 
            artist_catalog.img_url_sml)
    return results

def latest_daily_date(chart_model):
    latest_date = chart_model.query.order_by(chart_model.id.desc()).first().date
    return latest_date

def latest_daily_chart(chart_model):
    latest_date = latest_daily_date(chart_model)

    tracks = daily_chart_joined_art_cat(
        chart_model,
        latest_date
        )
    return tracks

def archive_chart_context(
        chart_model,
        year, month, day):

    url_date_string = f'{year}-{month}-{day}'
    records = daily_chart_joined_art_cat(
        chart_model,
        url_date_string
    )
    if not records:
        # Custom message when no data is found
        return "No data found for the specified date."
    
    if chart_model == daily_tracks:
        chart_type = 'Tracks'
    elif chart_model == daily_artists:
        chart_type = 'Artists'
    else:
        chart_type = None

    context = {
        'chart_type' : chart_type,
        'records' : records,
        'date' : url_date_string,
        'year' : year,
        'month' : month,
        'day' : day,
    }
    return context