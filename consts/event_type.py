class EventType(object):
    REGIONAL = 0
    DISTRICT = 1
    DISTRICT_CMP = 2
    CMP_DIVISION = 3
    CMP_FINALS = 4
    OFFSEASON = 99
    PRESEASON = 100
    UNLABLED = -1

    type_names = {
        REGIONAL: 'Regional',
        DISTRICT: 'District',
        DISTRICT_CMP: 'District Championship',
        CMP_DIVISION: 'Championship Division',
        CMP_FINALS: 'Championship Finals',
        OFFSEASON: 'Offseason',
        PRESEASON: 'Preseason',
        UNLABLED: '--',
    }

    type_names_short = {
        REGIONAL: 'Regional',
        DISTRICT: 'District',
        DISTRICT_CMP: 'District CMP',
        CMP_DIVISION: 'Division',
        CMP_FINALS: '',
        OFFSEASON: 'Offseason',
        PRESEASON: 'Preseason',
        UNLABLED: '--',
    }

    NON_CMP_EVENT_TYPES = {
        REGIONAL,
        DISTRICT,
        DISTRICT_CMP,
    }

    CMP_EVENT_TYPES = {
        CMP_DIVISION,
        CMP_FINALS,
    }
