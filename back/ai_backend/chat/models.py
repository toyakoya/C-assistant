from django.db import models
class ChatMessage(models.Model):
    website=models.CharField(max_length=100,primary_key=True)
    model_name=models.CharField(max_length=40)
    problem=models.TextField()
    code=models.TextField()
    runResult=models.CharField(max_length=40)
    examples = models.JSONField()  # 新增，直接存储结构化样例数据
    ans =models.TextField()
    messages=models.JSONField()  
    def __str__(self):
        return f"{self.website}: {self.problem[:20]}..."
# Create your models here.
