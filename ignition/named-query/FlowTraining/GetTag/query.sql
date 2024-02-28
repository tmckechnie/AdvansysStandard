Declare @Name varchar(200) = :Name
Declare @Description varchar(2000) = :Description
Declare @EngUnit varchar(20) = :EngUnit
Declare @TagID int = (Select top 1 TagID from Tag where Name = @Name)

if @TagID is null
Begin
	insert into Tag (Name,Description,EngUnit) values (@Name,@Description,@EngUnit)
	select @TagID = @@Identity
End
Select @TagID as TagID

