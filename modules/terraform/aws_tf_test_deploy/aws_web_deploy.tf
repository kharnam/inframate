// Deploy web server on AWS
resource "aws_instance" "web" {
  ami = "ami-0f65671a86f061fcd"
  instance_type = "t1.micro"
  tags {
    Name = "kharnam-test-terraform-web"
  }
}
