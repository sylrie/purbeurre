from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # min

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'pur_beurre_platform.my_cron_job'    # a unique code

    def do(self):
        print('ça marche!') 