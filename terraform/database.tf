resource "aws_db_instance" "taskoverflow" {
  allocated_storage      = 20
  max_allocated_storage  = 1000
  engine                 = "postgres"
  engine_version         = "14"
  instance_class         = "db.t4g.micro"
  db_name                = "ticketoverflow"
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = "default.postgres14"
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.database.id]
  publicly_accessible    = true

  tags = {
    Name = "ticketoverflow_database"
  }
}

resource "null_resource" "init_db" {
  depends_on = [aws_db_instance.taskoverflow]

  provisioner "local-exec" {
    command = "python3 ./database/init-db.py  ${aws_db_instance.taskoverflow.endpoint} ${aws_db_instance.taskoverflow.db_name} ${aws_db_instance.taskoverflow.username} ${aws_db_instance.taskoverflow.password} ./database/users.json"
  }
}