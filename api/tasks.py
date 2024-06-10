# api/tasks.py
from celery import shared_task
from .models import Job, Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(job_id, coin):
    job = Job.objects.get(id=job_id)
    task = Task.objects.create(job=job, coin=coin, status='in_progress')

    scraper = CoinMarketCap()
    data = scraper.get_coin_data(coin)
    scraper.close()

    task.data = data
    task.status = 'completed'
    task.save()
    return task.id,task.data
