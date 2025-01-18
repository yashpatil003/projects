from django.db import models

# Create your models here.
class Question(models.Model):
    
    qno=models.IntegerField(primary_key=True)
    qtext=models.CharField(max_length=100)
    answer=models.CharField(max_length=50)
    op1=models.CharField(max_length=50)
    op2=models.CharField(max_length=50)
    op3=models.CharField(max_length=50)
    op4=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.qno , self.qtext , self.answer,self.op1,self.op2}"
    
    class Meta:
        db_table="question"


