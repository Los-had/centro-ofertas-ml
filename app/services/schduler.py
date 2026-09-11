from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()


def scan_deals():
    print("Executando varredura de ofertas...")


scheduler.add_job(
    scan_deals,
    "interval",
    minutes=30,
)


if __name__ == "__main__":
    print("Scheduler iniciado.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()