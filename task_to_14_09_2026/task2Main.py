from task2Processes.monitorResults import monitor
import asyncio

import signal

async def main():
    # задача мониторинга
    monitor_task = asyncio.create_task(monitor())
    
    #  Ctrl+C для остановки
    def shutdown():
        print("\n Work done...")
        monitor_task.cancel()
    
    # обработчик сигнала
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)
    
    try:
        await monitor_task
    except asyncio.CancelledError:
        print("Monitoring finished")

if __name__ == "__main__":
    asyncio.run(main())
