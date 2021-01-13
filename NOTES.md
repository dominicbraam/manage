## Program to manage tasks

# Objectives
Create tasks
Allow tasks to have duration (add time onto existing time), subtasks
Use MySQL Database to store data.
Read data and output filtered info.

# Database


# To-do
Let a new table be created for each year
Add status: "recurring"


# Tasks Table
Columns: tasID, task, subtask, duration, date stamp, status, task list


ALTER TABLE ReferencingTable DROP 
   CONSTRAINT fk__ReferencingTable__MainTable;

ALTER TABLE ReferencingTable ADD 
   CONSTRAINT fk__ReferencingTable__MainTable 
      FOREIGN KEY (pk_col_1)
      REFERENCES MainTable (pk_col_1)
      ON DELETE CASCADE ON UPDATE CASCADE;

	  *can add update cascade

# To reset primary keys
SET @count = 0;

UPDATE `user`  SET `user_id` = @count:= @count + 1;

ALTER TABLE `user_id` AUTO_INCREMENT = 1;
