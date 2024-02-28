SELECT TOP 1 tpts.TimePeriodID
FROM TimePeriodTimeScheme as tpts
inner join TimePeriod as tp on tp.TimePeriodID = tpts.TimePeriodID


where tpts.TimeSchemeID =  :CalendarID  and
tp.IntervalTypeID = 8 -- Year Enumeration ID

order by PeriodEnd desc