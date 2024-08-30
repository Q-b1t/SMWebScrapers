from datetime import datetime
import pytz
import re



def get_date_type(date):
  # date patterns as throws by the scrappers
  regex_1 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}') # works for facebook
  regex_2 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z') # works for tik tok & instagram
  regex_3 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z') # works for youtube
  regex_4 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}') # works for x
  if regex_1.match(date) is not None:
    if regex_2.match(date) is not None:
      return 'type2'
    elif regex_3.match(date) is not None:
      return 'type3'
    else:
      return 'type1'
  else:
    return 'type4'
  
def format_date(date,input_format,output_format = "%Y-%m-%d %H:%M:%S",timezone='America/Mexico_City'):
    #Convertir a zona horario de mexico para coincida con los demás
    # Fecha en UTC
    utc_time = datetime.strptime(date, input_format) # "%Y-%m-%dT%H:%M:%S.%fZ"

    # Zona horaria de México (por ejemplo, Ciudad de México)
    mexico_tz = pytz.timezone(timezone)

    # Convertir la hora UTC a la zona horaria de México
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(mexico_tz)

    # Mostrar la fecha y hora convertida sin la zona horaria
    createdat = local_time.strftime(output_format)
    return createdat


def normalize_date(date,output_format = "%Y-%m-%d %H:%M:%S",timezone='America/Mexico_City'):
  date_input_formats = {
    'type1':"%Y-%m-%dT%H:%M:%S",
    'type2':"%Y-%m-%dT%H:%M:%S.%fZ",
    "type3":"%Y-%m-%dT%H:%M:%SZ",
    "type4":"%Y-%m-%d %H:%M:%S"
  }
  date_type = get_date_type(date)
  formated_date = format_date(
      date=date,
      input_format=date_input_formats[date_type],
      output_format = output_format,
      timezone=timezone
  )
  return formated_date