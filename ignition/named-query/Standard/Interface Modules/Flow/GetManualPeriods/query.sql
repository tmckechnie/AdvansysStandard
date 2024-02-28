Declare @IntervalTypeID int = :IntervalTypeID
Declare @CalendarID int = :CalendarID
Declare @PeriodStart datetime2 = :PeriodStartUTC
Select PeriodStart=cast(PeriodStart as Datetime),PeriodEnd = cast(PeriodEnd as Datetime) from TimePeriod tp 
join TimePeriodTimeScheme tpts on tpts.TimePeriodID = tp.TimePeriodID
where tpts.TimeSchemeID = @CalendarID and IntervalTypeID = @IntervalTypeID and PeriodStart>=@PeriodStart
order by PeriodStart