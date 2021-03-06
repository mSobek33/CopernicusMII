import sys, time
import datetime
from Ingestion.classes import ParameterHandler
from Ingestion.classes import ElasticSearchHandler
from Ingestion.classes import COPlogger


log = COPlogger('UpdateAt')
paramHandler = ParameterHandler(log.logger, 'config.ini')
config = paramHandler.setConfig()

ces = ElasticSearchHandler(log.logger, 'elastic', 'elastic')

#ces.getAllItem()

# Frage 1M Gruppe ab
    # BBOX: NOT POLYGON((-5.578 35.945, -1.909 36.679, 2.585 38.893, 11.447 38.703, 11.821 34.903, 33.794 34.452, 34.673 35.711, 29.449 35.550, 29.446 35.550, 29.445 35.550, 29.444 35.550, 29.443 35.550, 29.443 35.550, 27.119 37.784, 26.554 39.398, 25.422 40.204, 28.295 42.110, 29.531 44.300, 35.651 44.300, 39.957 47.821, 40.553 49.783, 33.610 52.645, 31.149 55.975, 28.424 56.609, 28.600 60.718, 32.204 62.956, 29.479 68.753, 31.325 69.750, 31.325 70.467, 31.201 78.938, 37.310 80.171, 20.426 80.803, 9.6158 79.797, 10.143 78.225, 17.974 75.590, 19.028 71.145, -6.468 71.245, -9.456 71.189, -9.984 70.496, 17.614 70.614, 10.583 67.341, 6.012 63.550, -12.444 63.706, -11.390 65.948, -16.488 66.862, -22.926 66.628, -24.579 65.500, -22.772 63.667, -18.729 63.255, -7.743 63.056, -7.743 57.846, -10.555 54.215, -10.819 52.000, -10.555 39.608, -31.275 39.743, -31.275 39.302, -25.057 36.803, -25.046 36.803, -17.235 32.623, -18.333 27.608, -18.333 27.589, -15.521 27.6476, -13.7856 28.094, -13.126 29.231, -16.136 33.213, -17.652 32.974, -24.793 36.794, -24.760 39.582, -10.555 39.489, -9.588 36.671, -6.248 35.927, -5.578 35.945))
    # NOT Archived
    # Älter als 1M
    # HAT CODE-DE Link
# Frage 12M Gruppe ab
    # BBOX: POLYGON((-5.578 35.945, -1.909 36.679, 2.585 38.893, 11.447 38.703, 11.821 34.903, 33.794 34.452, 34.673 35.711, 29.449 35.550, 29.446 35.550, 29.445 35.550, 29.444 35.550, 29.443 35.550, 29.443 35.550, 27.119 37.784, 26.554 39.398, 25.422 40.204, 28.295 42.110, 29.531 44.300, 35.651 44.300, 39.957 47.821, 40.553 49.783, 33.610 52.645, 31.149 55.975, 28.424 56.609, 28.600 60.718, 32.204 62.956, 29.479 68.753, 31.325 69.750, 31.325 70.467, 31.201 78.938, 37.310 80.171, 20.426 80.803, 9.6158 79.797, 10.143 78.225, 17.974 75.590, 19.028 71.145, -6.468 71.245, -9.456 71.189, -9.984 70.496, 17.614 70.614, 10.583 67.341, 6.012 63.550, -12.444 63.706, -11.390 65.948, -16.488 66.862, -22.926 66.628, -24.579 65.500, -22.772 63.667, -18.729 63.255, -7.743 63.056, -7.743 57.846, -10.555 54.215, -10.819 52.000, -10.555 39.608, -31.275 39.743, -31.275 39.302, -25.057 36.803, -25.046 36.803, -17.235 32.623, -18.333 27.608, -18.333 27.589, -15.521 27.6476, -13.7856 28.094, -13.126 29.231, -16.136 33.213, -17.652 32.974, -24.793 36.794, -24.760 39.582, -10.555 39.489, -9.588 36.671, -6.248 35.927, -5.578 35.945))
    # NOT Archived
    # Älter als 12M
    # HAT CODE-DE Link
# Frage 36M Gruppe ab
    # BBOX: POLYGON((5.47 45.77, 17.25 45.77, 17.28 55.05, 5.47 55.05, 5.47 45.77))
    # NOT Archived
    # Älter als 12M
    # HAT CODE-DE Link


# Ermittel Datum vor 6 Monaten
d6 = datetime.datetime.now()
a6 = d6.replace(
    year=d6.year if d6.month > 1 else d6.year - 1,
    month=d6.month - 6 if d6.month > 1 else 12,
)
print(a6.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

# Ermittel Datum vor 36 Monaten
d36 = datetime.datetime.now()
a36 = d36.replace(
    year=d36.year - 3
)
print(a36.strftime("%Y-%m-%dT%H:%M:%S.000Z"))