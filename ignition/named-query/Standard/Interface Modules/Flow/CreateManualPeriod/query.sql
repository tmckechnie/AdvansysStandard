Declare		@CalendarName VARCHAR(200) =  :CalendarName 
Declare		@IntervalType VARCHAR(10) =  :IntervalType 
Declare		@PeriodStart DATETIME2 =  :PeriodStart 
Declare		@PeriodEnd DATETIME2 =  :PeriodEnd 
Declare		@LocalTime BIT = 1

exec CreateManualTimePeriod @CalendarName,@IntervalType,@PeriodStart,@PeriodEnd,@LocalTime
